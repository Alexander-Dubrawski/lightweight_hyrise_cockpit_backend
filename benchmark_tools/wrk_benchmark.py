"""Tool for executing wrk benchmark."""
from multiprocessing import Manager, Process
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .wrk_benchmark_helper import (
    create_folder,
    format_results,
    plot_results,
    print_results,
    write_to_csv,
)

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 30
ENDPOINTS = ["workload", "database", "queue_length", "storage", "throughput", "latency"]


def execute_wrk_on_endpoint(url):
    """Background process to execute wrk."""
    return check_output(
        f"wrk -t1 -c1 --latency -d{DURATION_IN_SECOUNDS}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def wrk_background_process(url, endpoint, shared_data):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"wrk -t1 -c1 --latency -d{DURATION_IN_SECOUNDS}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def create_wrk_processes(shared_data):
    """Create one wrk process per endpoint."""
    return [
        Process(
            target=wrk_background_process,
            args=(f"{BACKEND_URL}/{end_point}", end_point, shared_data),
        )
        for end_point in ENDPOINTS
    ]


def run_wrk_sequential():
    """Run wrk sequential on all endpoints."""
    sequential_results = {}
    for endpoint in ENDPOINTS:
        sequential_results[endpoint] = execute_wrk_on_endpoint(
            f"{BACKEND_URL}/{endpoint}"
        )
    return sequential_results


def run_wrk_parallel():
    """Run wrk in parallel on all endpoints."""
    manager = Manager()
    shard_dict = manager.dict()
    processes = create_wrk_processes(shard_dict)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()
    parallel_results = {}
    for key, value in shard_dict.items():
        parallel_results[key] = value
    return parallel_results


def run_benchmark():
    """Run sequential and parallel wrk benchmark on endpoints."""
    sequential_results = run_wrk_sequential()
    parallel_results = run_wrk_parallel()
    print_results(sequential_results, parallel_results)
    formatted_sequential_results = format_results(sequential_results)
    formatted_parallel_results = format_results(parallel_results)
    path = create_folder("wrk_benchmark")
    plot_results(path, formatted_sequential_results, formatted_parallel_results)
    write_to_csv(formatted_sequential_results, formatted_parallel_results, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
