"""Server module handling zmq requests.

Used by Database Manager and Workload Generator.
"""

from json import dumps, loads
from typing import Dict

from backend.request import Request
from backend.response import Response, get_response
from zmq import POLLIN, ROUTER, Context, Poller


class Server:
    """Server component handling zmq requests."""

    def __init__(self, host: str, port: str, calls: Dict, io_threads: int = 1,) -> None:
        """Initialize a Server with a host, port and calls."""
        self._calls = calls
        self._host = host
        self._port = port
        self._init_server(io_threads)

    def _init_server(self, io_threads: int) -> None:
        self._context = Context(io_threads=io_threads)
        self._client = self._context.socket(ROUTER)
        self._client.bind("tcp://{:s}:{:s}".format(self._host, self._port))
        self._poller = Poller()
        self._poller.register(self._client, POLLIN)

    def start(self) -> None:
        """Start the server loop."""
        while True:
            socks = dict(self._poller.poll())

            if socks.get(self._client) == POLLIN:
                multi_part_message = self._client.recv_multipart()
                identity, delimeter_fram, data = multi_part_message
                request: Request = loads(data.decode("utf-8"))
                response: Response = self._handle_request(request)
                json_string = dumps(response)
                self._client.send_multipart(
                    [identity, delimeter_fram, json_string.encode()]
                )

    def _handle_request(self, request: Request) -> Response:
        try:
            func = self._calls[request["header"]["message"]]
            return func(request["body"])
        except KeyError:
            return get_response(404)

    def close(self) -> None:
        """Close the socket and terminate it."""
        self._client.close()
        self._context.term()
