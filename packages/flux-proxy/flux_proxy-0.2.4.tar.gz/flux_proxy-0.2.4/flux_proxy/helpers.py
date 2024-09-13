import asyncio
import functools

from flux_proxy.auth import SignatureAuthProvider
from flux_proxy.log import log
from flux_proxy.rpc_client import RPCClient
from flux_proxy.symbols import (AUTH_ADDRESS_REQUIRED, AUTH_DENIED, NO_SOCKET,
                                PROXY_AUTH_ADDRESS_REQUIRED, PROXY_AUTH_DENIED)
from flux_proxy.transport.client_transport import \
    EncryptedSocketClientTransport


async def handle_session(transport: EncryptedSocketClientTransport):
    if transport.session.started:
        if not transport.session.connection_attempted:
            await transport.session.start(connect=True)

            # if signing_address := transport.session.signing_address:
            #     signing_key = await asyncio.to_thread(
            #         keyring.get_password, "fluxvault_app", signing_address
            #     )

            #     if not signing_key:
            #         log.error(
            #             f"Signing key required in keyring for {signing_address}"
            #         )
            #         # fix this no address
            #         raise FluxVaultKeyError(
            #             f"Reason: {transport.failed_on} Signing key not present in secure storage"
            #         )

            #     await transport.session.connect(signing_key)


async def handle_connection(
    transport: EncryptedSocketClientTransport,
    connect: bool,
    exclusive: bool = False,
) -> int | None:
    if connect:
        chan_id = await transport.connect(
            exclusive=exclusive
        )  # this gives us exclusive use of channel
        if transport.connected:
            return chan_id

    if not transport.connected:
        log.info(
            "Transport not connected... checking connection requirements..."
        )
        log.info(f"Failed on {transport.failed_on}")

        if transport.failed_on == NO_SOCKET:
            return

        # address = ""
        # # match/case
        # if transport.failed_on in [AUTH_ADDRESS_REQUIRED, AUTH_DENIED]:
        #     address = "auth_address"
        # elif transport.failed_on in [
        #     PROXY_AUTH_ADDRESS_REQUIRED,
        #     PROXY_AUTH_DENIED,
        # ]:
        #     address = "proxy_auth_address"

        # signing_key = keyring.get_password(
        #     "fluxvault_app", getattr(transport, address)
        # )

        # if not signing_key:
        #     log.error(
        #         f"Signing key required in keyring for {getattr(transport, address)}"
        #     )
        #     raise FluxVaultKeyError(
        #         f"Reason: {transport.failed_on} Signing key for address: {getattr(transport, address)} not present in secure storage"
        #     )

        # auth_provider = SignatureAuthProvider(key=signing_key)
        # transport.auth_provider = auth_provider

        return await transport.connect(exclusive=exclusive)


def manage_transport(f=None, exclusive: bool = False):
    def inner(f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            # Surely there is a better way
            agent = None
            for arg in args:
                if isinstance(arg, RPCClient):
                    agent = arg
                    break

            transport: EncryptedSocketClientTransport = agent.transport

            disconnect = kwargs.pop("disconnect", True)
            connect = kwargs.pop("connect", True)
            in_session = kwargs.pop("in_session", False)

            log.debug(
                f"In wrapper for {f.__name__}, connect: {connect}, disconnect: {disconnect}, in_session: {in_session} agent: {agent.id}"
            )

            if in_session:
                # this doesn't actually return a chan_id (it should)
                chan_id = await handle_session(transport)
            else:
                chan_id = await handle_connection(transport, connect, exclusive)

            if not transport.connected:
                log.error(f"{agent.id}: Connection failed... returning")
                return

            res = await f(*args, **kwargs)

            if not in_session and disconnect:
                await transport.disconnect(chan_id)

            return res

        return wrapper

    if f:
        return inner(f)
    else:
        return inner
