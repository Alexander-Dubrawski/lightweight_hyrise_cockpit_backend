"""Service for back-end api."""
from typing import List

from backend.request import Header, Request
from backend.response import Response

from .interface import DatabaseInterface, DetailedDatabaseInterface, WorkloadInterface
from .model import DetailedDatabase, Workload
from .socket_manager import GeneratorSocket, ManagerSocket


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


class DatabaseService:
    """Services of the Database Controller."""

    @staticmethod
    def _send_message_to_dbm(message: Request) -> Response:
        """Send an IPC message to the database manager."""
        with ManagerSocket() as socket:
            return socket.send_message(message)

    @classmethod
    def get_databases(cls) -> List[DetailedDatabase]:
        """Get all Databases.

        Returns a list of all databases with detailed information.
        """
        response = cls._send_message_to_dbm(
            Request(header=Header(message="get databases"), body={})
        )
        return [
            DetailedDatabase(**interface) for interface in response["body"]["databases"]
        ]

    @classmethod
    def register_database(cls, interface: DetailedDatabaseInterface) -> int:
        """Add a database to the manager."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="add database"), body=dict(interface))
        )
        return response["header"]["status"]

    @classmethod
    def deregister_database(cls, interface: DatabaseInterface) -> int:
        """Remove database from manager."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="delete database"), body=dict(interface))
        )
        return response["header"]["status"]
