"""Service for back-end api."""

from backend.request import Header, Request
from backend.response import Response

from .interface import WorkloadInterface
from .model import Workload
from .socket_manager import GeneratorSocket


class WorkloadService:
    """Services of the Workload Controller."""

    @staticmethod
    def _send_message_to_gen(message: Request) -> Response:
        """Send an IPC message to the workload generator."""
        with GeneratorSocket() as socket:
            return socket.send_message(message)

    @classmethod
    def get_workload(cls) -> Workload:
        """Get all Workloads.
        Returns the running Workloads.
        """
        response = cls._send_message_to_gen(
            Request(header=Header(message="get workload"), body={}),
        )
        return Workload(**response["body"]["workload"])

    @classmethod
    def create(cls, interface: WorkloadInterface) -> int:
        """Create a Workload."""
        response = cls._send_message_to_gen(
            Request(header=Header(message="start workload"), body=dict(interface)),
        )
        return response["header"]["status"]

    @classmethod
    def delete(cls) -> int:
        """Stop a Workload."""
        response = cls._send_message_to_gen(
            Request(header=Header(message="stop workload"), body={}),
        )
        return response["header"]["status"]
