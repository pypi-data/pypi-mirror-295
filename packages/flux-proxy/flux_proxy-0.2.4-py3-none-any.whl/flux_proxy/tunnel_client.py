from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from functools import total_ordering
from json.decoder import JSONDecodeError
from math import asin, cos, radians, sin, sqrt
from socket import AF_INET
from typing import Any

from aiohttp import (
    ClientConnectorError,
    ClientSession,
    ClientTimeout,
    TCPConnector,
)

from flux_proxy.protocol_jsonrpc import JSONRPCProtocol
from flux_proxy.rpc_client import RPCClient
from flux_proxy.transport.client_transport import EncryptedSocketClientTransport


@dataclass
@total_ordering
class Location:
    lat: float
    lon: float
    query: str
    origin_lat: float
    origin_lon: float
    distance: float = field(init=False)

    @staticmethod
    def _calculate_distance(lon1: float, lat1: float, lon2: float, lat2: float):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        R = 6372.8  # Earth Radius km

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
        c = 2 * asin(sqrt(a))

        return R * c

    def __post_init__(self):
        self.distance = Location._calculate_distance(
            self.lat, self.lon, self.origin_lat, self.origin_lon
        )

    def __lt__(self, other: Location) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: Location) -> bool:
        return self.distance == other.distance


class TunnelClient:
    @staticmethod
    async def get_external_ip(retry_forever=False, max_attempts=3) -> str:
        providers = ["ifconfig.me", "api.ipify.org", "ipshow.me"]

        attempts_remaining = max_attempts
        timeout = ClientTimeout(connect=1)
        conn = TCPConnector(family=AF_INET)
        # ifconfig.me is weird - they use the UA header for text
        headers = {"Accept": "*/*", "User-Agent": "curl/8.6.0"}

        ip = ""

        async def get_first_response():
            data = ""

            async with ClientSession(
                connector=conn, headers=headers
            ) as session:

                for provider in providers:
                    url = f"https://{provider}"

                    try:
                        async with session.get(url, timeout=timeout) as resp:
                            if resp.status in [429, 500, 502, 503, 504]:
                                print(f"bad response {resp.status}... retrying")
                                continue

                            data = await resp.text()
                            break

                    except ClientConnectorError:
                        print(f"Unable to connect to {url}... retrying")
                        continue

            return data

        while not ip:
            ip = await get_first_response()

            if not retry_forever:
                attempts_remaining -= 1

                if not attempts_remaining:
                    break

        return ip

    @staticmethod
    def sort_closest(local: dict, coordinates: list[dict]) -> list:
        locs = [Location(**x, **local) for x in coordinates]
        locs.sort()

        return [x.query for x in locs]

    @staticmethod
    async def do_http(
        url: str,
        method: str = "get",
        *,
        data: Any = None,
        connect_timeout: int = 3,
        max_tries: int = 3,
    ):
        timeout = ClientTimeout(connect=connect_timeout)
        conn = TCPConnector(family=AF_INET)

        res = None

        async with ClientSession(
            connector=conn,
        ) as session:
            for _ in range(max_tries):
                try:
                    method = getattr(session, method)
                    async with method(url, timeout=timeout, json=data) as resp:
                        if resp.status in [429, 500, 502, 503, 504]:
                            print(f"bad response {resp.status}... retrying")
                            continue

                        try:
                            res = await resp.json()
                        except JSONDecodeError:
                            res = None
                        break

                except ClientConnectorError:
                    print(f"Unable to connect to {url}... retrying")
                    continue

        return res

    def __init__(
        self,
        *,
        flux_app_name: str,
        rpc_remote_port: int,
        http_local_endpoint: str,
    ) -> None:
        self.flux_app_name = flux_app_name
        self.rpc_remote_port = rpc_remote_port
        self.http_local_endpoint = http_local_endpoint

        self.proxy_url: str | None = None
        self.proxy_url_event = asyncio.Event()
        self.runner: asyncio.Task | None = None

        self.transport: EncryptedSocketClientTransport | None = None
        self.rpc_client: RPCClient | None = None

    async def _run(self) -> None:
        ips_task = self.get_proxy_ips()
        external_ip_task = TunnelClient.get_external_ip()

        proxy_ips, external_ip = await asyncio.gather(
            ips_task, external_ip_task
        )

        coords = await self.get_app_coordinates([external_ip, *proxy_ips])
        local_coords, other_coords = coords[0], coords[1:]

        origin = {
            "origin_lat": local_coords["lat"],
            "origin_lon": local_coords["lon"],
        }

        sorted_addresses = TunnelClient.sort_closest(origin, other_coords)

        # this will connect to the first address it can, i.e. the closest
        self.transport = EncryptedSocketClientTransport(
            sorted_addresses,
            self.rpc_remote_port,
            rekey_timer=60,
            debug=True,
        )

        self.rpc_client = RPCClient(JSONRPCProtocol(), self.transport)

        async with self.rpc_client.transport.session:
            # A session automatically sends keepalives every 30 seconds
            proxy = self.rpc_client.get_proxy()

            self.proxy_url = await proxy.register_endpoint(
                target=self.http_local_endpoint
            )
            self.proxy_url_event.set()

            # fix this
            await asyncio.wait([asyncio.Future()])

    async def run_forever(self) -> None:
        try:
            await self.runner
        except asyncio.CancelledError:
            pass

    async def clean_up(self) -> None:
        self.runner.cancel()

        try:
            await self.runner
        except asyncio.CancelledError:
            pass

    async def start_proxy(self) -> None:
        self.runner = asyncio.create_task(self._run())
        await self.proxy_url_event.wait()
        return self.proxy_url

    async def get_proxy_ips(self) -> list:
        url = f"https://api.runonflux.io/apps/location/{self.flux_app_name}"

        res = await self.do_http(url)

        if not res:
            return []

        try:
            status = res.get("status", None)
            data = res.get("data", [])

        except AttributeError:
            return []

        if status != "success":
            return []

        ips = [x.get("ip", "").partition(":")[0] for x in data]

        return list(filter(None, ips))

    async def get_app_coordinates(self, ips: list[str]) -> dict:
        url = "http://ip-api.com/batch?fields=query,lat,lon"

        res = await self.do_http(url, "post", data=ips)

        return res if res else {}
