from json import loads
from multiprocessing import Process
from threading import Thread
from time import sleep
from types import TracebackType
from typing import List, Optional, Type

from zmq import DEALER, POLLIN, REP, ROUTER, Context, Poller, proxy

from backend.database_manager.manager import DatabaseManager
from backend.request import Body, Request
from backend.response import Response, get_response


def _call_metric(body: Body) -> Response:
    # do some work
    sleep(0.05)
    response = get_response(200)
    return response


def worker_thread(url_thread, context=None):
    server_calls = {
        "get metric": _call_metric,
    }
    context = context or Context.instance()
    socket = context.socket(REP)
    socket.connect(url_thread)

    while True:
        request = socket.recv_json()
        call = request["header"]["message"]
        func = server_calls[call]
        socket.send_json(func(request["body"]))


def worker_proxy(number_threads, url_broker):
    url_thread = "inproc://threads"
    context = Context.instance()
    broker = context.socket(ROUTER)
    broker.connect(url_broker)
    threads = context.socket(DEALER)
    threads.bind(url_thread)

    for i in range(number_threads):
        thread = Thread(target=worker_thread, args=(url_thread,))
        thread.start()

    proxy(broker, threads)


def start_database_manager(
    db_manager_listening, db_manager_port, workload_sub_host, workload_pubsub_port
):

    with DatabaseManager(
        db_manager_listening, db_manager_port, workload_sub_host, workload_pubsub_port
    ) as manager:
        manager.start()


class Broker:
    def __init__(
        self,
        db_manager_listening: str,
        db_manager_port: str,
        broker_listening: str,
        broker_port: str,
        worker_listening: str,
        worker_port: str,
        workload_sub_host: str,
        workload_pubsub_port: str,
        mumber_worker: int,
        number_threads: int,
    ) -> None:
        self._db_manager_listening = db_manager_listening
        self._db_manager_port = db_manager_port
        self._broker_port = broker_port
        self._broker_listening = broker_listening
        self._worker_listening = worker_listening
        self._worker_port = worker_port
        self._database_manager_calls = [
            "add database",
            "delete database",
            "start worker",
            "close worker",
            "get databases",
            "get queue length",
            "status",
        ]
        self._init_server(1)
        self._database_manager_obj = Process(
            target=start_database_manager,
            args=(
                db_manager_listening,
                db_manager_port,
                workload_sub_host,
                workload_pubsub_port,
            ),
        )
        self._database_manager_obj.start()
        self._workers: List = self._start_worker(
            mumber_worker,
            number_threads,
            "tcp://127.0.0.1:{:s}".format(self._worker_port),
        )

    def __enter__(self) -> "Broker":
        """Return self for a context manager."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Call close with a context manager."""
        self.close()
        return None

    def _init_server(self, io_threads: int):
        self._context = Context(io_threads=io_threads)
        self._client = self._context.socket(ROUTER)
        self._client.bind("tcp://127.0.0.1:{:s}".format(self._broker_port))
        self._worker = self._context.socket(DEALER)
        self._worker.bind("tcp://127.0.0.1:{:s}".format(self._worker_port))
        self._database_manager = self._context.socket(DEALER)
        self._database_manager.bind(
            "tcp://127.0.0.1:{:s}".format(self._db_manager_port)
        )

        self._poller = Poller()
        self._poller.register(self._client, POLLIN)
        self._poller.register(self._worker, POLLIN)
        self._poller.register(self._database_manager, POLLIN)

    def _start_worker(self, mumber_worker, number_threads, url_broker) -> List:
        workers = []
        for i in range(number_threads):
            worker = Process(target=worker_proxy, args=(number_threads, url_broker,))
            worker.start()
            workers.append(worker)
        return workers

    def run(self) -> None:
        """Start the server loop."""
        while True:
            socks = dict(self._poller.poll())

            if socks.get(self._client) == POLLIN:
                multi_part_message = self._client.recv_multipart()
                identity, delimeter_fram, data = multi_part_message
                request: Request = loads(data.decode("utf-8"))
                call = request["header"]["message"]
                if call in self._database_manager_calls:
                    print(call)
                    self._database_manager.send_multipart(multi_part_message)
                else:
                    self._worker.send_multipart(multi_part_message)

            if socks.get(self._worker) == POLLIN:
                message = self._worker.recv_multipart()
                self._client.send_multipart(message)

            if socks.get(self._database_manager) == POLLIN:
                message = self._database_manager.recv_multipart()
                self._client.send_multipart(message)

    def close(self) -> None:
        # clean up
        self._database_manager_obj.terminate()
        self._client.close()
        self._worker.close()
        self._database_manager.close()
        self._context.term()
