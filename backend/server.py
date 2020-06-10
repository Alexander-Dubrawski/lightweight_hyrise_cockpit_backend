"""Server module handling zmq requests.

Used by Database Manager and Workload Generator.
"""

from json import dumps, loads
from multiprocessing import Process
from time import sleep
from typing import Dict

from backend.request import Body, Request
from backend.response import Response, get_response
from zmq import DEALER, POLLIN, REP, ROUTER, Context, Poller

NUMBER_WORKER = 16


def _call_time_intense_metric(body: Body) -> Response:
    # do some work
    sleep(0.2)
    response = get_response(200)
    return response


def _call_metric(body: Body) -> Response:
    # do some work
    sleep(0.001)
    response = get_response(200)
    return response


def worker_routine(host, port):
    server_calls = {
        "get time intense metric": _call_time_intense_metric,
        "get metric": _call_metric,
    }
    context = Context()
    socket = context.socket(REP)
    socket.connect("tcp://127.0.0.1:{:s}".format(port))

    while True:
        request = socket.recv_json()
        call = request["header"]["message"]
        if call == "KILL":
            break
        func = server_calls[call]
        socket.send_json(func(request["body"]))

    socket.close()
    context.term()


class Server:
    """Server component handling zmq requests."""

    def __init__(
        self,
        host: str,
        server_port: str,
        server_calls: Dict,
        worker_port: str,
        io_threads: int = 1,
    ) -> None:
        """Initialize a Server with a host, port and calls."""
        self._server_calls = server_calls
        self._host = host
        self._server_port = server_port
        self._worker_port = worker_port
        self._worker_processes = []  # type: ignore
        self._init_server(io_threads)

    def _init_server(self, io_threads: int) -> None:
        self._context = Context(io_threads=io_threads)
        self._client = self._context.socket(ROUTER)
        self._client.bind("tcp://{:s}:{:s}".format(self._host, self._server_port))
        self._worker = self._context.socket(DEALER)
        self._worker.bind("tcp://*:{:s}".format(self._worker_port))

        self._poller = Poller()
        self._poller.register(self._client, POLLIN)
        self._poller.register(self._worker, POLLIN)

        for _ in range(NUMBER_WORKER):
            p = Process(target=worker_routine, args=(self._host, self._worker_port,))
            p.start()
            self._worker_processes.append(p)

    def start(self) -> None:
        """Start the server loop."""
        while True:
            socks = dict(self._poller.poll())

            if socks.get(self._client) == POLLIN:
                multi_part_message = self._client.recv_multipart()
                identity, delimeter_fram, data = multi_part_message
                request: Request = loads(data.decode("utf-8"))
                call = request["header"]["message"]
                if call in self._server_calls.keys():
                    response: Response = self._handle_request(request)
                    json_string = dumps(response)
                    self._client.send_multipart(
                        [identity, delimeter_fram, json_string.encode()]
                    )
                else:
                    self._worker.send_multipart(multi_part_message)

            if socks.get(self._worker) == POLLIN:
                message = self._worker.recv_multipart()
                self._client.send_multipart(message)

    def _handle_request(self, request: Request) -> Response:
        try:
            func = self._server_calls[request["header"]["message"]]
            return func(request["body"])
        except KeyError:
            return get_response(404)

    def close(self) -> None:
        """Close the socket and terminate it."""
        self._client.close()
        self._context.term()
        for worker in self._worker_processes:
            worker.terminate()
