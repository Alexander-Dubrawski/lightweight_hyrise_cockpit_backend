"""Model for back-end api."""


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
        self, id: str, number_workers: int,
    ):
        """Initialize a Database model."""
        self.id: str = id
        self.number_workers: int = number_workers


class Status:
    """Model of a status."""

    def __init__(self, id: str, worker_pool_status: str):
        """Initialize a status model."""
        self.id: str = id
        self.worker_pool_status: str = worker_pool_status
