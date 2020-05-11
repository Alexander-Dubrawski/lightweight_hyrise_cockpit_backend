"""Interface for back-end api."""

from typing import List, TypedDict


class WorkloadInterface(TypedDict):
    """Interface of a Workload."""

    workload_name: str
    frequency: int


class DatabaseInterface(TypedDict):
    """Interface of a Database."""

    id: str


class DetailedDatabaseInterface(DatabaseInterface):
    """Interface of a detailed database."""

    host: str
    port: str
    number_workers: int
    dbname: str
    user: str
    password: str


class SqlQueryInterface(TypedDict):
    """Interface of a Sql query."""

    id: str
    query: str


class SqlResponseInterface(TypedDict):
    """Interface of a SQL query response."""

    id: str
    results: List[List[str]]
