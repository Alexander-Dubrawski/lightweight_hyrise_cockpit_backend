"""Service for back-end api."""
from time import sleep
from typing import Dict, List, Tuple

from backend.request import Header, Request
from backend.response import Response

from .interface import (
    DatabaseInterface,
    DetailedDatabaseInterface,
    SqlQueryInterface,
    WorkloadInterface,
)
from .model import DetailedDatabase, SqlResponse, Status, Workload
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

    @classmethod
    def start_worker_pool(cls) -> int:
        """Start worker pool."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="start worker"), body={})
        )
        return response["header"]["status"]

    @classmethod
    def close_worker_pool(cls) -> int:
        """Close worker pool."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="close worker"), body={})
        )
        return response["header"]["status"]

    @classmethod
    def get_status(cls) -> List[Status]:
        """Close worker pool."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="status"), body={})
        )
        return [Status(**interface) for interface in response["body"]["status"]]

    @classmethod
    def execute_sql(cls, interface: SqlQueryInterface) -> Tuple:
        """Execute sql query."""
        response = cls._send_message_to_dbm(
            Request(header=Header(message="execute sql query"), body=dict(interface))
        )
        if response["header"]["status"] == 200:
            return (
                SqlResponse(**response["body"]["results"]),
                200,
            )
        return response["header"]["status"]

    @classmethod
    def get_storage(cls) -> List[Dict]:
        """Execute sql query."""
        databases = DatabaseService.get_databases()
        # Do some work (access inluxDB)
        sleep(0.001)
        fake_storage_information = {
            "customer": {"size": 10000, "number_columns": 2},
            "supplier": {"size": 400, "number_columns": 1},
        }
        return [
            {"id": database.id, "results": fake_storage_information}
            for database in databases
        ]
