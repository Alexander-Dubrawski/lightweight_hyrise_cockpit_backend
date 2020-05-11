"""The database object represents the instance of a database."""
from typing import Dict

from .background_scheduler import BackgroundJobManager
from .worker_pool.pool import WorkerPool


class Database(object):
    """Represents database."""

    def __init__(
        self,
        id: str,
        host: str,
        port: str,
        number_workers: int,
        workload_publisher_url: str,
    ) -> None:
        """Initialize database object."""
        self._id = id
        self.number_workers: int = number_workers
        self.connection_information: Dict[str, str] = {
            "host": host,
            "port": port,
        }
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

    def execute_sql_query(self, query) -> Dict:
        """Execute sql query on database."""
        return {"id": self._id, "results": [["42", "foo"], ["Hallo", "World"]]}

    def close(self) -> None:
        """Close the database."""
        self._worker_pool.terminate()
        self._background_scheduler.close()
