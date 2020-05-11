"""Module for generating workloads.

Includes the main WorkloadGenerator.
"""

from types import TracebackType
from typing import Dict, Optional, Type

from apscheduler.schedulers.background import BackgroundScheduler
from zmq import PUB, Context

from backend.request import Body
from backend.response import Response, get_response
from backend.server import Server


class WorkloadGenerator(object):
    """Object responsible for generating workload."""

    def __init__(
        self,
        generator_listening: str,
        generator_port: str,
        workload_listening: str,
        workload_pub_port: str,
    ) -> None:
        """Initialize a WorkloadGenerator."""
        self._workload_listening = workload_listening
        self._workload_pub_port = workload_pub_port
        server_calls: Dict = {
            "start workload": self._call_start_workload,
            "get workload": self._call_get_workload,
            "stop workload": self._call_stop_workload,
        }
        self._server = Server(generator_listening, generator_port, server_calls)
        self._workload: str = None  # type: ignore
        self._workload_frequency: int = 0
        self._init_server()
        self._init_scheduler()

    def _init_scheduler(self) -> None:
        self._scheduler = BackgroundScheduler()
        self._generate_workload_job = self._scheduler.add_job(
            func=self._generate_workload, trigger="interval", seconds=1,
        )
        self._scheduler.start()

    def __enter__(self) -> "WorkloadGenerator":
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

    def _init_server(self) -> None:
        self._context = Context(io_threads=1)
        self._pub_socket = self._context.socket(PUB)
        self._pub_socket.bind(
            "tcp://{:s}:{:s}".format(self._workload_listening, self._workload_pub_port)
        )

    def _call_start_workload(self, body: Body) -> Response:
        self._workload = body["workload_name"]
        self._workload_frequency = body["frequency"]
        return get_response(200)

    def _call_stop_workload(self, body: Body) -> Response:
        self._workload = None  # type: ignore
        self._workload_frequency = 0
        return get_response(200)

    def _generate_workload(self) -> None:
        if self._workload:
            response = get_response(200)
            response["body"]["querylist"] = [
                self._workload for _ in range(self._workload_frequency)
            ]
            self._pub_socket.send_json(response)

    def _call_get_workload(self, body: Body) -> Response:
        response = get_response(200)
        response["body"]["workload"] = {
            "workload_name": self._workload,
            "frequency": self._workload_frequency,
        }
        return response

    def start(self) -> None:
        """Start the generator by starting the server."""
        self._server.start()

    def close(self) -> None:
        """Close the socket and context."""
        self._generate_workload_job.remove()
        self._scheduler.shutdown()
        self._pub_socket.close()
        self._context.term()
