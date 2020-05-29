"""Interface for back-end api."""

from typing import TypedDict


class WorkloadInterface(TypedDict):
    """Interface of a Workload."""

    workload_name: str
    frequency: int


class DatabaseInterface(TypedDict):
    """Interface of a Database."""

    id: str


class DetailedDatabaseInterface(DatabaseInterface):
    """Interface of a detailed database."""

    number_workers: int
