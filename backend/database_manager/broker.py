# flake8: noqa
from json import dumps, loads
from multiprocessing import Process
from threading import Thread
from time import sleep
from types import TracebackType
from typing import List, Optional, Type

from backend.database_manager.manager import DatabaseManager
from backend.request import Body, Request
from backend.response import Response, get_response
from zmq import DEALER, IDENTITY, POLLIN, REQ, ROUTER, Context, Poller


def _call_metric(body: Body) -> Response:
    # do some work
    sleep(0.05)
    response = get_response(200)
    return response


def worker_thread(url_thread, context=None):
    server_calls = {
        "get metric": _call_metric,
    }
    context = Context.instance()
    socket = context.socket(REQ)
    socket.connect(url_thread)
    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        (
            broker_address,
            empty_frame,
            client_address,
            empty_frame,
            client_request,
        ) = socket.recv_multipart()
        request = loads(client_request.decode("utf-8"))
        call = request["header"]["message"]
        func = server_calls[call]
        results = func(request["body"])
        formatted_results = dumps(results)
        socket.send_multipart(
            [broker_address, b"", client_address, b"", formatted_results.encode()]
        )


def worker_proxy(broker_id, number_threads, worker_id, url_broker):
    context = Context.instance()
    broker = context.socket(ROUTER)
    byte_worker_id = f"WORKER_{worker_id}".encode()
    broker.setsockopt(IDENTITY, byte_worker_id)
    broker.connect(url_broker)
    thread = context.socket(ROUTER)
    thread.bind("inproc://threads")

    threads_obj = []
    for i in range(number_threads):
        t = Thread(target=worker_thread, args=("inproc://threads",))
        t.start()
        threads_obj.append(t)

    poller = Poller()
    poller.register(thread, POLLIN)
    threads = []
    init = True
    poller.register(broker, POLLIN)

    while True:
        sockets = dict(poller.poll())

        if thread in sockets:
            # Handle worker activity on the backend
            request = thread.recv_multipart()
            # we need to unpack the last three values. This is the inner envelop
            thread_address, empty_frame, broker_address = request[:3]
            threads.append(thread_address)
            print("ready")
            if broker_address != b"READY" and len(request) > 3:
                # If client reply, send rest back to broker
                (
                    thread_address,
                    empty_frame,
                    broker_address,
                    empty_frame,
                    client_address,
                    empty_frame,
                    cleint_reply,
                ) = request
                broker.send_multipart(
                    [broker_address, b"", client_address, b"", cleint_reply]
                )

        if broker in sockets:
            # Get next client request, route to last-used worker
            message = broker.recv_multipart()
            (
                broker_address,
                empty_frame,
                client_address,
                empty_frame,
                client_request,
            ) = message
            thread_address = threads.pop(0)
            thread.send_multipart(
                [
                    thread_address,
                    b"",
                    broker_address,
                    b"",
                    client_address,
                    b"",
                    client_request,
                ]
            )


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
        self._worker = self._context.socket(ROUTER)
        self._worker.setsockopt(IDENTITY, b"BROKER")
        self._worker.bind("tcp://127.0.0.1:{:s}".format(self._worker_port))
        self._database_manager = self._context.socket(DEALER)
        self._database_manager.bind(
            "tcp://127.0.0.1:{:s}".format(self._db_manager_port)
        )
        self._worker_addresses: List = []
        self._poller = Poller()
        # self._poller.register(self._client, POLLIN)
        self._poller.register(self._worker, POLLIN)
        self._poller.register(self._database_manager, POLLIN)

    def _start_worker(self, number_worker, number_threads, url_broker) -> List:
        workers = []
        for i in range(number_worker):
            worker = Process(
                target=worker_proxy, args=(b"BROKER", number_threads, i, url_broker,)
            )
            worker.start()
            workers.append(worker)
            for _ in range(number_threads):
                self._worker_addresses.append(f"WORKER_{i}".encode())
        return workers

    def run(self) -> None:
        """Start the server loop."""
        self._poller.register(self._client, POLLIN)
        while True:
            socks = dict(self._poller.poll())

            if self._worker in socks:
                request = self._worker.recv_multipart()
                worker_address, empty_frame, client_adress = request[:3]
                if not self._worker_addresses:
                    # Poll for clients now that a worker is available
                    self._poller.register(self._client, POLLIN)
                self._worker_addresses.append(worker_address)
                empty_frame, cleint_reply = request[3:]
                self._client.send_multipart([client_adress, b"", cleint_reply])

            if socks.get(self._client) == POLLIN:
                multi_part_message = self._client.recv_multipart()
                client_adress, empty_frame, client_request = multi_part_message
                req: Request = loads(client_request.decode("utf-8"))
                call = req["header"]["message"]
                if call in self._database_manager_calls:
                    self._database_manager.send_multipart(multi_part_message)
                else:
                    worker_address = self._worker_addresses.pop(0)
                    self._worker.send_multipart(
                        [worker_address, b"", client_adress, b"", client_request]
                    )
                    if not self._worker_addresses:
                        # Don't poll clients if no workers are available
                        self._poller.unregister(self._client)

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
