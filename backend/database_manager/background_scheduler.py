"""The BackgroundJobManager is managing the background jobs for the apscheduler."""
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler


def update_queue_length():
    """Update queue length."""
    # Do some work
    sleep(0.1)


def update_system_data():
    """Update system data."""
    # Do some work
    sleep(0.5)


class BackgroundJobManager(object):
    """Manage background scheduling jobs."""

    def __init__(self):
        """Initialize BackgroundJobManager object."""
        self._scheduler: BackgroundScheduler = BackgroundScheduler()
        self._init_jobs()

    def _init_jobs(self) -> None:
        """Initialize basic background jobs."""
        self._update_queue_length_job = self._scheduler.add_job(
            func=update_queue_length, trigger="interval", seconds=1,
        )
        self._update_system_data_job = self._scheduler.add_job(
            func=update_system_data, trigger="interval", seconds=1,
        )

    def start(self) -> None:
        """Start background scheduler."""
        self._scheduler.start()

    def close(self) -> None:
        """Close background scheduler."""
        self._update_system_data_job.remove()
        self._update_queue_length_job.remove()
        self._scheduler.shutdown()
