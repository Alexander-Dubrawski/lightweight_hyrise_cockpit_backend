"""The WorkerPool object represents the workers."""
from multiprocessing import Event, Process, Value
from multiprocessing.synchronize import Event as EventType
from typing import List, Optional

from apscheduler.schedulers.background import BackgroundScheduler

from backend.cross_platform_support.multiprocessing_support import Queue

from .enqueue_worker import enqueue_worker
from .execute_worker import execute_worker


class WorkerPool:
    """Represents WorkerPool."""

    def __init__(
        self, number_worker: int, database_id: str, workload_publisher_url: str,
    ) -> None:
        """Initialize WorkerPool object."""
        self._number_worker: int = number_worker
        self._database_id: str = database_id
        self._workload_publisher_url: str = workload_publisher_url
        self._status: str = "closed"
        self._continue_execution_flag: Value = Value("b", True)
        self._execute_workers: List[Process] = []
        self._execute_task_worker_done_event: List[EventType] = []
        self._enqueue_worker: Optional[Process] = None
        self._worker_wait_for_exit_event: EventType = Event()
        self._task_queue: Queue = Queue(0)
        self._scheduler: BackgroundScheduler = BackgroundScheduler()
        self._scheduler.start()

    def _generate_execute_worker_done_events(self) -> List[EventType]:
        return [Event() for _ in range(self._number_worker)]

    def _generate_execute_worker(self) -> List[Process]:
        return [
            Process(
                target=execute_worker,
                args=(
                    self._task_queue,
                    self._continue_execution_flag,
                    self._execute_task_worker_done_event[i],
                    self._worker_wait_for_exit_event,
                ),
            )
            for i in range(self._number_worker)
        ]

    def _generate_enqueue_worker(self) -> Process:
        return Process(
            target=enqueue_worker,
            args=(
                self._workload_publisher_url,
                self._task_queue,
                self._continue_execution_flag,
                self._worker_wait_for_exit_event,
            ),
        )

    def _init_workers(self) -> None:
        self._execute_task_worker_done_event = (
            self._generate_execute_worker_done_events()
        )
        self._execute_workers = self._generate_execute_worker()
        self._enqueue_worker = self._generate_enqueue_worker()

    def _terminate_worker(self) -> None:
        self._enqueue_worker.terminate()  # type: ignore
        self._enqueue_worker = None
        for i in range(self._number_worker):
            self._execute_workers[i].terminate()
        self._execute_workers = []
        self._worker_wait_for_exit_event = Event()
        self._task_queue = Queue(0)

    def _wait_for_worker(self) -> None:
        self._worker_wait_for_exit_event.clear()
        self._continue_execution_flag.value = False
        for i in range(self._number_worker):
            self._execute_task_worker_done_event[i].wait()

    def _start_worker(self) -> None:
        self._continue_execution_flag.value = True
        self._enqueue_worker.start()  # type: ignore
        for i in range(self._number_worker):
            self._execute_workers[i].start()

    def _start_job(self) -> None:
        if self._status == "closed":
            self._worker_wait_for_exit_event.set()
            self._init_workers()
            self._start_worker()
            self._status = "running"

    def _close_job(self) -> None:
        if self._status == "running":
            self._wait_for_worker()
            self._terminate_worker()
        self._status = "closed"

    def start(self) -> bool:
        """Start worker."""
        self._scheduler.add_job(func=self._start_job)
        return True

    def close(self) -> bool:
        """Close worker."""
        self._scheduler.add_job(func=self._close_job)
        return True

    def terminate(self) -> bool:
        """Terminates worker."""
        if self._status == "running":
            self._terminate_worker()
            self._task_queue.close()
            self._status = "closed"
            return True
        else:
            return False

    def get_status(self) -> str:
        """Return status of pool."""
        return self._status

    def get_queue_length(self) -> int:
        """Return queue length."""
        return self._task_queue.qsize()
