"""Model for back-end api."""

from typing import List


class Workload:
    """Model of a Workload."""

    def __init__(self, workload_name: str, frequency: int):
        """Initialize a Workload model."""
        self.workload_name: str = workload_name
        self.frequency: int = frequency


class Database:
    """Model of a Database."""

    def __init__(self, id: str):
        """Initialize a Database model."""
        self.id: str = id


class DetailedDatabase:
    """Model of a detailed Database."""

    def __init__(
        self, id: str, host: str, port: str, number_workers: int,
    ):
        """Initialize a Database model."""
        self.id: str = id
        self.host: str = host
        self.port: str = port
        self.number_workers: int = number_workers


class Status:
    """Model of a status."""

    def __init__(self, id: str, worker_pool_status: str):
        """Initialize a status model."""
        self.id: str = id
        self.worker_pool_status: str = worker_pool_status


class SqlQuery:
    """Model of a sql query."""

    def __init__(self, id: str, query: str):
        """Initialize a sql query model."""
        self.id: str = id
        self.query: str = query


class SqlResponse:
    """Model of a sql query response."""

    def __init__(
        self, id: str, results: List[List[str]],
    ):
        """Initialize a sql response model."""
        self.id: str = id
        self.results: List[List[str]] = results


class QueueLength:
    """Model of a queue length response."""

    def __init__(
        self, id: str, queue_length: int,
    ):
        """Initialize a queue length response model."""
        self.id: str = id
        self.queue_length: int = queue_length
