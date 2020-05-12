"""Tool for executing wrk benchmark in multiple processes."""

import subprocess  # nosec
from multiprocessing import Process

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 10
ENDPOINTS = ["worklaod", "database", "queue_length", "storage", "throughput", "latency"]


def wrk_background_process(url):
    """Background process to execute wrk."""
    sub_process = subprocess.run(  # nosec
        ["wrk", "-t1", "-c1", f"-d{DURATION_IN_SECOUNDS}s", f"{url}"],
        capture_output=True,
    )
    print(sub_process.stdout.decode("utf-8"))
    print(sub_process.stderr.decode("utf-8"))


def create_wrk_processes():
    """Create one wrk process per endpoint."""
    return [
        Process(target=wrk_background_process, args=(f"{BACKEND_URL}/{end_point}",),)
        for end_point in ENDPOINTS
    ]


def run_benchmark():
    """Run wrk benchmark on endpoints."""
    processes = create_wrk_processes()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
