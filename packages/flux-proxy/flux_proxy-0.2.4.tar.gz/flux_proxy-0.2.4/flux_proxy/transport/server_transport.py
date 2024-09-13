from __future__ import annotations  # 3.10 style

import asyncio
import binascii
import fcntl
import io
import os
import re
import select
import signal
import ssl

# pty stuff
import struct
import tarfile
import termios
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, BinaryIO

import aiofiles
import bson
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

from flux_proxy.auth import (
    AuthProvider,
    AuthReplyMessage,
    ChallengeReplyMessage,
)
from flux_proxy.log import log
from flux_proxy.messages import (
    AesRekeyMessage,
    ChallengeMessage,
    EncryptedMessage,
    FileEntryStreamMessage,
    HttpErrorMessage,
    HttpRequestMessage,
    HttpResponseBeginMessage,
    HttpResponseDataMessage,
    LivelinessMessage,
    ProxyMessage,
    ProxyResponseMessage,
    PtyClosedMessage,
    PtyMessage,
    PtyResizeMessage,
    RpcReplyMessage,
    RpcRequestMessage,
    RsaPublicKeyMessage,
    SerializedMessage,
    SessionKeyMessage,
    TestMessage,
)


def bytes_to_human(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


@dataclass
class KeyData:
    aes_key: str = ""
    rsa_private: str = ""
    rsa_public: str = ""

    def burn_rsa_keys(self):
        self.rsa_private = ""
        self.rsa_public = ""

    def generate(self):
        rsa_key = RSA.generate(2048)
        self.rsa_private = rsa_key.export_key()
        self.rsa_public = rsa_key.publickey().export_key()


@dataclass
class EncryptablePeerGroup:
    peers: list[EncryptablePeer] = field(default_factory=list)

    def __len__(self):
        return len(self.peers)

    def __iter__(self):
        yield from self.peers

    async def destroy_peer(self, id):
        log.info(f"Destroying peer: {id}")
        peer: EncryptablePeer = self.get_peer(id)
        if peer:
            peer.read_socket_task.cancel()
            for task in peer.in_flight_messages:
                task.cancel()

            try:
                peer.writer.close()
                await peer.writer.wait_closed()
            except (ConnectionResetError, BrokenPipeError):
                pass

            self.peers = [x for x in self.peers if x.id != id]

    async def destroy_peer_timer(self, id, timeout):
        await asyncio.sleep(timeout)
        log.debug(f"Destroying peer{id}, timed out")
        await self.destroy_peer(id)

    def get_peer(self, id):
        for peer in self.peers:
            if peer.id == id:
                return peer

    def add_peer(self, peer):
        self.peers.append(peer)

    async def destroy_all_peers(self):
        try:
            for peer in self.peers:
                await self.destroy_peer(peer.id)
        except Exception as e:
            print("destroy all peers exception")
            print(repr(e))

    def start_peer_timeout(self, id):
        peer = self.get_peer(id)
        timeout = 10

        peer.timer = asyncio.create_task(
            self.destroy_peer_timer(peer.id, timeout)
        )


@dataclass
class Channel:
    """A dedicated message queue to segregate messages per flow on the socket"""

    id: int
    exclusive: bool = False
    in_use: bool = False
    # use a bounded queue, if we don't and we get a large inflow of messages, rest of app will get
    # starved as q.put() will just go ham
    q: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=5))


@dataclass
class EncryptablePeer:
    id: tuple
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    key_data: KeyData = field(default_factory=KeyData)
    encrypted: bool = False
    authenticated: bool = False
    separator = b"<?!!?>"
    # ToDo: multiple ptys
    pty: BinaryIO | None = None
    pid: int = 0
    random: str = ""
    proxied: bool = False
    timer: asyncio.Task | None = None
    read_socket_task: asyncio.Task | None = None
    in_flight_messages: list[asyncio.Task] = field(default_factory=list)
    challenge_complete_event: asyncio.Event = field(
        default_factory=asyncio.Event
    )
    forwarding_event: asyncio.Event = field(default_factory=asyncio.Event)
    fh: dict[str, BinaryIO] = field(default_factory=dict)
    http_channels: list[Channel] = field(
        default_factory=lambda: [Channel(id=0), Channel(id=1)]
    )

    def add_channel(self, exclusive: bool) -> Channel:
        id = self.http_channels[-1].id + 1
        channel = Channel(id=id, exclusive=exclusive)
        self.http_channels.append(channel)
        return channel

    def get_channel_by_id(self, id) -> Channel | None:
        return next(filter(lambda x: x.id == id, self.http_channels), None)

    def get_channel(
        self, chan_id: int | None = None, exclusive: bool = False
    ) -> Channel | None:
        if chan_id:
            return self.get_channel_by_id(chan_id)

        elif exclusive:
            chan: Channel = next(
                filter(
                    lambda x: not x.in_use and x.exclusive, self.http_channels
                ),
                None,
            )

        else:
            chan: Channel | None = next(
                filter(
                    lambda x: not x.in_use and not x.exclusive,
                    self.http_channels,
                ),
                None,
            )

        if not chan:
            chan = self.add_channel(exclusive=exclusive)

        chan.in_use = True
        return chan

    async def send(self, msg: bytes):
        log.debug(f"Sending message: {bson.decode(msg)}")
        self.writer.write(msg + self.separator)
        await self.writer.drain()

    # shouldn't this be run in executor?
    # async def write_tarfile(self, path: Path, tar: tarfile.TarFile):
    #     tar.extractall(str(path))
    #     tar.close()
    #     self.fh = None

    async def handle_file_stream_message(self, msg: FileEntryStreamMessage):
        if msg.path not in self.fh:
            log.info(f"Server transport: New file stream received {msg.path}")
            p = Path(msg.path)
            p.parent.mkdir(parents=True, exist_ok=True)
            self.fh[msg.path] = await aiofiles.open(p, "wb")
            # tar = tarfile.open(fileobj=self.fh, mode="r|bz2")
            # asyncio.create_task(self.write_tarfile(msg.path, tar))

        # this has to be first so empty files created
        await self.fh[msg.path].write(msg.data)

        if msg.eof:
            log.info(
                f"Server transport: Stream file EOF received for {msg.path} ... closing handle"
            )
            await self.fh[msg.path].close()
            del self.fh[msg.path]
            return

    async def handle_http_message(
        self,
        msg: (
            HttpResponseBeginMessage
            | HttpResponseDataMessage
            | HttpErrorMessage
        ),
    ):
        chan = self.get_channel_by_id(msg.id)
        if not chan:
            return

        await chan.q.put(msg)

    def handle_pty_message(self, msg):
        if not self.pty:
            return

        if isinstance(msg, PtyResizeMessage):
            self.set_winsize(msg.rows, msg.cols)
        else:
            os.write(self.pty, msg.data)

    def set_winsize(self, row, col, xpix=0, ypix=0):
        log.debug("setting window size with termios")
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(self.pty, termios.TIOCSWINSZ, winsize)

    async def proxy_pty(self, separator: bytes):
        max_read_bytes = 1024 * 20

        while True:
            if not self.pty:
                log.warn("Remote end closed pty. Cleaning up...")
                break
            if self.pty:
                timeout_sec = 0
                data_ready, _, _ = select.select(
                    [self.pty], [], [], timeout_sec
                )
                if data_ready:
                    output = os.read(self.pty, max_read_bytes)
                    # this happens when subprocess closed
                    if output == b"":
                        log.warn(
                            "No output from read after select. Pty closed... cleaning up"
                        )
                        self.pty = None
                        self.pid = 0
                        break
                    # ToDo: should this be buffered?
                    msg = PtyMessage(output)
                    msg = msg.encrypt(self.key_data.aes_key)
                    self.writer.write(msg.serialize() + separator)
                    await self.writer.drain()
                    continue  # skip sleep if data (might be more data)
            await asyncio.sleep(0.01)

        log.info("Sending Pty closed message")
        msg = PtyClosedMessage(b"Process exited")
        msg = msg.encrypt(self.key_data.aes_key)
        self.writer.write(msg.serialize() + separator)
        try:
            await self.writer.drain()
        except Exception as e:  # Tighten
            log.error("error draining proxy pty in finally")
            log.error(repr(e))


class ServerTransport:
    """Abstract base class for all server transports.

    The server side implementation of the transport component.
    Requests and replies encoded by the protocol component are
    exchanged between client and server using the :py:class:`ServerTransport`
    and :py:class:`ClientTransport` classes.
    """

    def receive_message(self) -> tuple[Any, bytes]:
        """Receive a message from the transport.

        Blocks until a message has been received.
        May return an opaque context object to its caller that should be passed on to
        :py:func:`~tinyrpc.transport.ServerTransport.send_reply` to identify
        the transport or requester later on.
        Use and function of the context object are entirely controlled by the transport
        instance.

        The message must be treated as a binary entity as only the protocol
        level will know how to interpret the message.

        If the transport encodes the message in some way, the opposite end
        is responsible for decoding it before it is passed to either client
        or server.

        :return: A tuple consisting of ``(context, message)``.
            Where ``context`` can be any valid Python type and
            ``message`` must be a :py:class:`bytes` object.
        """
        raise NotImplementedError()


class EncryptedSocketServerTransport(ServerTransport):
    def __init__(
        self,
        address: str,
        port: int,
        whitelisted_addresses: list = [],
        verify_source_address: bool = True,
        auth_provider: AuthProvider | None = None,
        ssl: ssl.SSLContext | None = None,
        debug: bool = False,
    ):
        self._address = address
        self._port = port
        self.is_async = True
        self.debug = debug
        self.peers = EncryptablePeerGroup()
        self.rpc_messages = asyncio.Queue(maxsize=5)
        # not used??
        # self.control_messages = asyncio.Queue()
        self.separator = b"<?!!?>"
        # ToDo: validate addresses
        self.whitelisted_addresses = whitelisted_addresses
        self.verify_source_address = verify_source_address
        self.auth_provider = auth_provider
        self.ssl = ssl

    def parse_session_key_message(
        self, key_pem: str, msg: SessionKeyMessage
    ) -> str:
        """Used by Node to decrypt and return the AES Session key using the RSA Key"""
        try:
            private_key = RSA.import_key(key_pem)

            enc_session_key = msg.rsa_encrypted_session_key

            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)

            enc_aes_key_message = SerializedMessage(
                msg.aes_key_message
            ).deserialize()

            aes_key_message = enc_aes_key_message.decrypt(session_key)
        except Exception as e:
            print(repr(e))
            print("trower")
            exit(0)

        return aes_key_message.aes_key

    async def begin_encryption(
        self, peer: EncryptablePeer, rekey: bool = False
    ):
        # this can take 0.5 seconds to generate (on macbook), have to run in thread to avoid blocking loop
        await asyncio.to_thread(peer.key_data.generate)
        msg = RsaPublicKeyMessage(peer.key_data.rsa_public)

        try:
            if rekey:
                msg = msg.encrypt(peer.key_data.aes_key)

            await peer.send(msg.serialize())
            self.peers.start_peer_timeout(peer.id)
        except Exception as e:
            print(repr(e))
            exit("bye")

    async def send_challenge_message(self, peer: EncryptablePeer) -> bool:
        source = peer.writer.get_extra_info("sockname")

        msg = ChallengeMessage(
            source=source, auth_required=bool(self.auth_provider)
        )

        if self.auth_provider:
            msg = self.auth_provider.generate_challenge(msg)

        await peer.send(msg.serialize())
        self.peers.start_peer_timeout(peer.id)

    async def valid_source_ip(self, peer_ip) -> bool:
        """Called when connection is established to verify correct source IP"""
        if peer_ip not in self.whitelisted_addresses:
            # Delaying here doesn't really stop against a DoS attack so have lowered
            # this to 3 seconds. In fact, it makes it even easier to DoS as you have an
            # open socket consuming resources / port
            await asyncio.sleep(3)
            log.warning(
                f"Reject Connection, wrong IP: {peer_ip} Expected {self.whitelisted_addresses}"
            )
            return False
        return True

    async def handle_auth_message(
        self, peer: EncryptablePeer, msg: ChallengeReplyMessage
    ):
        peer.timer.cancel()
        source = peer.writer.get_extra_info("sockname")

        if msg.close_connection:
            # client handler will do this destroy peer
            log.info("Client requested close connection... closing")
            peer.challenge_complete_event.set()
            return

        if not self.auth_provider:
            log.info("No auth required by ourselves, continue")
            peer.challenge_complete_event.set()
            return

        peer.authenticated = self.auth_provider.verify_auth(msg)
        resp = AuthReplyMessage(source=source, authenticated=peer.authenticated)

        await peer.send(resp.serialize())

        log.info(f"Auth provider authenticated: {peer.authenticated}")
        peer.challenge_complete_event.set()

    async def handle_liveliness_message(
        self, peer: EncryptablePeer, msg: LivelinessMessage
    ):
        reply = LivelinessMessage(msg.chan_id, msg.text[::-1])
        reply = reply.encrypt(peer.key_data.aes_key)

        await peer.send(reply.serialize())

    async def handle_aes_rekey_message(
        self, peer: EncryptablePeer, msg: AesRekeyMessage
    ):
        # still figuring what to, is there any content in this message?
        try:
            await self.begin_encryption(peer, rekey=True)
        except Exception as e:
            print(repr(e))
            exit("peace")

    async def handle_forwarding_message(
        self, peer: EncryptablePeer, msg: ProxyMessage
    ):
        resp = ProxyResponseMessage(False)
        if msg.proxy_required:
            success, proxy_id = await self.setup_forwarding(
                msg.proxy_target, msg.proxy_port, peer
            )
            resp.success = success
            resp.socket_details = proxy_id
            log.debug("Response message")
            log.debug(resp)
            await peer.send(resp.serialize())

            if not success:
                log.error("Not proxied... closing socket")
                await self.peers.destroy_peer(peer.id)

            peer.forwarding_event.set()

            return

        await peer.send(resp.serialize())
        peer.forwarding_event.set()

    async def handle_encryption_message(
        self, peer: EncryptablePeer, msg: SessionKeyMessage | EncryptedMessage
    ):
        if peer.timer:
            peer.timer.cancel()

        if isinstance(msg, SessionKeyMessage):
            aes_key = self.parse_session_key_message(
                peer.key_data.rsa_private, msg
            )

            peer.key_data.aes_key = aes_key

            peer.key_data.burn_rsa_keys()

            if not peer.encrypted:
                # Send a test encryption request, always include random data
                peer.random = get_random_bytes(16).hex()
                test_msg = TestMessage(peer.random)
                encrypted_test_msg = test_msg.encrypt(aes_key)

                await peer.send(encrypted_test_msg.serialize())

        if isinstance(msg, EncryptedMessage):
            response = msg.decrypt(peer.key_data.aes_key)

            if (
                response.text == "TestEncryptionMessageResponse"
                and response.fill == peer.random[::-1]
            ):
                peer.encrypted = True
            log.info(f"Socket is encrypted: {peer.encrypted}")

    async def setup_forwarding(
        self, host: str, port: int, peer: EncryptablePeer
    ) -> tuple:
        """Connects to socket server. Tries a max of 3 times"""
        attempts = 3

        proxy_reader = proxy_writer = None
        for n in range(attempts):
            start = time.monotonic()

            try:
                async with asyncio.timeout(3):
                    proxy_reader, proxy_writer = await asyncio.open_connection(
                        host, port
                    )

                break

            except asyncio.TimeoutError:
                log.warn(f"Timeout error connecting to {host}")
            except ConnectionError:
                log.warn(f"Connection error connecting to {host}")
            except Exception as e:
                log.warn(f"Unknown exception {e} trying to proxy connction")

            elapsed = time.monotonic() - start

            await asyncio.sleep(max(0, 1 - elapsed))

        if proxy_writer:
            peer.proxied = True
            pipe1 = self.pipe(peer.reader, proxy_writer)
            pipe2 = self.pipe(
                proxy_reader, peer.writer, self.peers.destroy_peer, peer.id
            )

            # hold a reference to these tasks so they don't get gc'd.
            asyncio.create_task(pipe1)
            asyncio.create_task(pipe2)

            source = peer.writer.get_extra_info("sockname")
            proxy_source = proxy_writer.get_extra_info("sockname")

            log.info(
                f"Proxy path: {peer.id} <-> {source} <-> {proxy_source} <-> ({host}, {port})"
            )

            return True, proxy_source
        return False, None

    async def proxy_pty(self, peer_id):
        log.info(
            "Received proxy pty request... forwarding local pty to remote socket"
        )
        peer = self.peers.get_peer(peer_id)

        task = peer.proxy_pty(self.separator)
        asyncio.create_task(task)

    # this is called externally, don't have access to peer object,
    # have to get it
    def attach_pty(self, pid, pty, peer_id):
        log.info(f"Attaching to pty for peer: {peer_id}")
        peer = self.peers.get_peer(peer_id)

        try:
            peer.pty = pty
            peer.pid = pid
        except Exception as e:
            print("in attach_pty")
            print(repr(e))

    def detach_pty(self, peer_id):
        log.info("detaching pty")
        peer = self.peers.get_peer(peer_id)

        peer.pty = None
        if peer.pid:
            os.kill(peer.pid, signal.SIGKILL)

    async def pipe(self, reader, writer, callback=None, id=""):
        try:
            while not reader.at_eof():
                writer.write(await reader.read(2048))
        finally:
            log.debug(f"Closing pipe for proxied connection")
            if callback:
                await callback(id)
            else:
                writer.close()
                await writer.wait_closed()

    async def handle_client(self, reader, writer):
        client_id = writer.get_extra_info("peername")
        log.info(f"Peer connected: {client_id}")

        peer = EncryptablePeer(client_id, reader, writer)
        self.peers.add_peer(peer)

        if self.verify_source_address and not await self.valid_source_ip(
            client_id[0]
        ):
            log.warn("Source IP address not verified... dropping")
            await self.peers.destroy_peer(peer.id)
            return

        peer.read_socket_task = asyncio.create_task(self.read_socket_loop(peer))

        await self.send_challenge_message(peer)

        await peer.challenge_complete_event.wait()
        peer.challenge_complete_event.clear()

        if not peer.authenticated and self.auth_provider:
            log.warn("Peer not authenticated... destroying socket")
            await self.peers.destroy_peer(peer.id)
            return

        await peer.forwarding_event.wait()
        peer.forwarding_event.clear()

        if peer.writer and not peer.writer.is_closing() and not peer.proxied:
            await self.begin_encryption(peer)

        log.info("Client bootstrap complete... read loop has control")

    async def overrun_strategy(self, peer: EncryptablePeer, to_consume: int):
        log.info(f"LimitOverrun: Read {bytes_to_human(to_consume)} into buffer")

        current = await peer.reader.read(to_consume)
        return current

    async def read_socket_loop(self, peer: EncryptablePeer):
        buffer = []
        while peer.reader and not peer.proxied and not peer.reader.at_eof():
            try:
                # this needs timeout
                data = await peer.reader.readuntil(separator=self.separator)
            except asyncio.exceptions.IncompleteReadError:
                log.debug(f"Reader is at EOF. Peer: {peer.id}")
                break
            except ConnectionResetError:
                log.warn(f"Connect was reset by peer: {peer.id}")
                # do we need to tidy up here?
                break
            except BrokenPipeError:
                # ToDo: fix this?
                log.error(f"Broken pipe")
                break
            except ConnectionError:
                log.warn(f"Connection Error to peer: {peer.id}")
                # do we need to tidy up here?
                break
            except asyncio.LimitOverrunError as e:
                buffer.append(await self.overrun_strategy(peer, e.consumed))
                continue
            except Exception as e:
                log.error(f"Unknown read socket error: {repr(e)}")
                break

            if buffer:
                buffer.extend([data, self.separator])
                data = b"".join(buffer)
                buffer = []

            message = data.rstrip(self.separator)

            t = asyncio.create_task(
                self.process_messages(peer, [message]), name=f"process_messages"
            )

            peer.in_flight_messages.append(t)

        log.debug(f"Read socket loop finished. peer.proxied: {peer.proxied}")
        if not peer.proxied:
            # reader at eof
            await self.peers.destroy_peer(peer.id)

    async def process_messages(
        self, peer: EncryptablePeer, messages: list[bytes]
    ):
        for message in messages:
            try:
                message = SerializedMessage(message).deserialize()
            except Exception as e:
                # ToDo: fix this
                log.error(repr(e))
                print("start", message[0:100])
                print("end", message[-100:])
                continue

            log.debug(f"Received : {type(message).__name__}")

            if peer.encrypted:
                try:
                    message = message.decrypt(peer.key_data.aes_key)
                except Exception as e:
                    print(repr(e))
                    print("can't decrypt")
                log.debug(f"Received decrypted: {type(message).__name__}")

            match message:
                case AesRekeyMessage():
                    await self.handle_aes_rekey_message(peer, message)

                case PtyMessage() | PtyResizeMessage():
                    peer.handle_pty_message(message)

                case (
                    HttpResponseBeginMessage()
                    | HttpResponseDataMessage()
                    | HttpErrorMessage()
                ):
                    await peer.handle_http_message(message)

                case FileEntryStreamMessage():
                    await peer.handle_file_stream_message(message)

                case LivelinessMessage():
                    await self.handle_liveliness_message(peer, message)

                case ChallengeReplyMessage():
                    await self.handle_auth_message(peer, message)

                # Encrypted message is the test message (peer isn't encrypted)
                case SessionKeyMessage() | EncryptedMessage():
                    await self.handle_encryption_message(peer, message)

                case ProxyMessage():
                    await self.handle_forwarding_message(peer, message)

                case RpcRequestMessage():
                    log.debug(
                        f"Message received (decrypted and decoded): {bson.decode(message.payload)})"
                    )
                    await self.rpc_messages.put(
                        (peer.id, message.chan_id, message.payload)
                    )

                case _:
                    log.error(f"Unknown message: {message}")

        # we hold a reference to the task in case the read socket loop ends and we have messages
        # still being processed - we ditch them as the socket is probably toast
        task = asyncio.current_task()
        peer.in_flight_messages.remove(task)

    async def stop_server(self):
        log.info("Stopping server")
        await self.peers.destroy_all_peers()
        log.info("after destroy peers")
        self.server.close()
        await self.server.wait_closed()

    async def start_server(self):
        started = False
        while not started:
            try:
                self.server = await asyncio.start_server(
                    self.handle_client,
                    self._address,
                    self._port,
                    ssl=self.ssl,
                    limit=1048576 * 105,
                    start_serving=True,
                )
                started = True
            except OSError as e:
                log.error(f"({e})... retrying in 5 seconds")
                await asyncio.sleep(5)

        addrs = ", ".join(
            str(sock.getsockname()) for sock in self.server.sockets
        )
        log.info(f"Serving on {addrs}")

    async def receive_message(self) -> tuple:
        addr, channel, message = await self.rpc_messages.get()
        # message = message.as_dict()
        return addr, channel, message

    async def get_http_response(
        self, context: tuple, chan_id: int
    ) -> HttpResponseBeginMessage | HttpResponseDataMessage | HttpErrorMessage:
        peer = self.peers.get_peer(context)
        chan = peer.get_channel_by_id(chan_id)

        msg: (
            HttpResponseBeginMessage
            | HttpResponseDataMessage
            | HttpErrorMessage
        ) = await chan.q.get()

        if isinstance(msg, HttpErrorMessage) or msg.eof:
            chan.in_use = False

        return msg

    async def send_http_message(
        self,
        context: tuple,
        path: str,
        method: str,
        body: str,
        headers: dict | None = None,
    ):
        if not headers:
            headers = {}

        peer = self.peers.get_peer(context)
        chan_id = peer.get_channel().id
        msg = HttpRequestMessage(chan_id, path, method, body, headers)

        if not peer:
            # socket has been terminated / removed
            log.warning(
                f"Peer {context} has been destroyed... dropping message"
            )
            return

        if peer.encrypted:
            msg = msg.encrypt(peer.key_data.aes_key)

        await peer.send(msg.serialize())

        return chan_id

    async def send_reply(self, context: tuple, channel: int, data: bytes):
        msg = RpcReplyMessage(channel, data)
        peer = self.peers.get_peer(context)

        if not peer:
            # socket has been terminated / removed
            log.warning(f"Peer {context} has been destroyed... dropping reply")
            return

        log.debug(
            f"Decoded RPC response (before encryption): {bson.decode(msg.payload)}"
        )
        # this should always be True
        if peer.encrypted:
            msg = msg.encrypt(peer.key_data.aes_key)

        await peer.send(msg.serialize())


if __name__ == "__main__":

    async def main():
        server = EncryptedSocketServerTransport(
            "127.0.0.1", 8888, verify_source_address=False, debug=True
        )
        await server.start_server()

        async with server.server:
            await server.server.serve_forever()

    asyncio.run(main())
