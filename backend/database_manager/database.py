"""The database object represents the instance of a database."""
from .background_scheduler import BackgroundJobManager
from .worker_pool.pool import WorkerPool


class Database(object):
    """Represents database."""

    def __init__(
        self, id: str, number_workers: int, workload_publisher_url: str,
    ) -> None:
        """Initialize database object."""
        self._id = id
        self.number_workers: int = number_workers
        self._worker_pool: WorkerPool = WorkerPool(
            self.number_workers, self._id, workload_publisher_url,
        )
        self._background_scheduler: BackgroundJobManager = BackgroundJobManager()
        self._background_scheduler.start()

    def get_queue_length(self) -> int:
        """Return queue length."""
        return self._worker_pool.get_queue_length()

    def get_worker_pool_status(self) -> str:
        """Return worker pool status."""
        return self._worker_pool.get_status()

    def start_worker(self) -> bool:
        """Start worker."""
        return self._worker_pool.start()

    def close_worker(self) -> bool:
        """Close worker."""
        return self._worker_pool.close()

    def close(self) -> None:
        """Close the database."""
        self._worker_pool.terminate()
        self._background_scheduler.close()
