"""Tool for executing scenario benchmark."""
from multiprocessing import Process
from subprocess import run  # nosec

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT
from requests import delete, post

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
NUMBER_DATABASES = 5
DURATION_IN_SECOUNDS = 60
ENDPOINTS = ["worklaod", "database", "queue_length", "storage", "throughput", "latency"]


def add_database(self, database_id: str):
    """Add database."""
    body = {
        "id": database_id,
        "host": "host",
        "port": "port",
        "number_workers": 8,
    }
    url = f"{BACKEND_URL}/database"
    return post(url, json=body)


def remove_database(self, database_id: str):
    """Add database."""
    body = {"id": database_id}
    url = f"{BACKEND_URL}/database"
    return delete(url, json=body)


def start_workload(self):
    """Start workload execution."""
    body = {"workload_name": "fake_workload", "frequency": 10000}
    url = f"{BACKEND_URL}/workload"
    return post(url, json=body)


def stop_workload(self, workload_folder: str):
    """Stop workload execution."""
    url = f"{BACKEND_URL}/workload"
    return delete(url)


def start_workers(self):
    """Start worker pool."""
    url = f"{BACKEND_URL}/worker"
    return post(url)


def stop_workers(self):
    """Stop worker pool."""
    url = f"{BACKEND_URL}/worker"
    return delete(url)


def wrk_background_process(url):
    """Background process to execute wrk."""
    sub_process = run(  # nosec
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


def run_wrk_benchmark():
    """Run wrk benchmark on endpoints."""
    processes = create_wrk_processes()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()


def run_benchmark():
    """Execute scenario steps"""
    total_response_time = 0
    for i in range(NUMBER_DATABASES):
        response = add_database(str(i))
        total_response_time = total_response_time + response.elapsed.total_seconds()
    print(f"Avg time to add database: {total_response_time / NUMBER_DATABASES}")

    response = start_workload()
    print(f"Time to start workload: {response.elapsed.total_seconds()}")

    response = start_workers()
    print(f"Time to start workers: {response.elapsed.total_seconds()}")

    run_wrk_benchmark()

    response = stop_workers()
    print(f"Time to stop workers: {response.elapsed.total_seconds()}")

    response = stop_workload()
    print(f"Time to stop workload: {response.elapsed.total_seconds()}")

    total_response_time = 0
    for i in range(NUMBER_DATABASES):
        response = remove_database(str(i))
        total_response_time = total_response_time + response.elapsed.total_seconds()
    print(f"Avg time to remove database: {total_response_time / NUMBER_DATABASES}")


if __name__ == "__main__":
    run_benchmark()  # type: ignore
