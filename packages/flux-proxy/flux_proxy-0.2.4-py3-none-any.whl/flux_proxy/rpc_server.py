import asyncio
from typing import Any

import flux_proxy.exceptions as exc
from flux_proxy.dispatcher import RPCDispatcher
from flux_proxy.protocol import RPCProtocol
from flux_proxy.transport.server_transport import ServerTransport


class RPCServer:
    """High level RPC server.
    The server is completely generic only assuming some form of RPC communication is intended.
    Protocol, data transport and method dispatching are injected into the server object.
    :param transport: The data transport mechanism to use.
    :param protocol: The RPC protocol to use.
    :param dispatcher: The dispatching mechanism to use.
    :type transport: :py:class:`~aiotinrypc.transports.ServerTransport`
    :type protocol: :py:class:`~aiotinrypc.protocols.RPCProtocol`
    :type dispatcher: :py:class:`~aiotinrypc.dispatch.RPCDispatcher`
    """

    trace = None
    """Trace incoming and outgoing messages.
    When this attribute is set to a callable this callable will be called directly
    after a message has been received and immediately after a reply is sent.
    The callable should accept three positional parameters:

    :param str direction: Either '-->' for incoming or '<--' for outgoing data.
    :param any context: The context returned by :py:meth:`~aiotinrypc.transports.ServerTransport.receive_message`.
    :param bytes message: The message itself.
    Example:

    .. code-block:: python
        def my_trace(direction, context, message):
            logger.debug('%s%s', direction, message)
        server = RPCServer(transport, protocol, dispatcher)
        server.trace = my_trace
        server.serve_forever()
    will log all incoming and outgoing traffic of the RPC service.

    Note that the ``message`` will be the data stream that is transported,
    not the interpreted meaning of that data.
    It is therefore possible that the binary stream is unreadable without further translation.
    """

    def __init__(
        self,
        transport: ServerTransport,
        protocol: RPCProtocol,
        dispatcher: RPCDispatcher,
    ):
        self.transport = transport
        self.protocol = protocol
        self.dispatcher = dispatcher
        self.trace = None

    async def serve_forever(self) -> None:
        """Handle requests forever.
        Starts the server loop; continuously calling :py:meth:`receive_one_message`
        to process the next incoming request.
        """
        if self.transport.is_async:
            # Catch?
            loop = asyncio.get_running_loop()
            loop.create_task(self.transport.start_server())

        while True:
            await self.receive_one_message()

    async def receive_one_message(self) -> None:
        """Handle a single request.
        Polls the transport for a new message.
        After a new message has arrived :py:meth:`_spawn` is called with a handler
        function and arguments to handle the request.
        The handler function will try to decode the message using the supplied
        protocol, if that fails, an error response will be sent. After decoding
        the message, the dispatcher will be asked to handle the resulting
        request and the return value (either an error or a result) will be sent
        back to the client using the transport.
        """
        if self.transport.is_async:
            context, channel, message = await self.transport.receive_message()
        else:
            context, channel, message = self.transport.receive_message()
        if callable(self.trace):
            self.trace("-->", context, message)

        loop = asyncio.get_running_loop()
        loop.create_task(self.handle_message(context, channel, message))

    async def handle_message(
        self, context: Any, channel: int, message: bytes
    ) -> None:
        """Parse, process and reply a single request."""
        try:
            request = self.protocol.parse_request(message)
        except exc.RPCError as e:
            response = e.error_respond()
        else:
            response = await self.dispatcher.dispatch(
                context, request, getattr(self.protocol, "_caller", None)
            )

        # send reply
        if response is not None:
            result = response.serialize()
            if callable(self.trace):
                self.trace("<--", context, result)
            if self.transport.is_async:
                await self.transport.send_reply(context, channel, result)
            else:
                self.transport.send_reply(context, channel, result)
