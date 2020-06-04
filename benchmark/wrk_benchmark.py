"""Tool for executing wrk benchmark."""
from multiprocessing import Manager, Process
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .wrk_benchmark_helper import (
    create_folder,
    format_results,
    plot_theoretical_charts,
    print_results,
)

NUMBER_CLIENTS = [1, 2, 8]
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 1
DURATION_IN_SECOUNDS_PARALLEL = 1
ENDPOINTS = ["manager_time_intense_metric", "manager_metric", "flask_metric"]


def execute_wrk_on_endpoint(url, number_clinets):
    """Background process to execute wrk."""
    return check_output(
        f"wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_SECOUNDS}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def wrk_background_process(url, endpoint, shared_data, number_clinets):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_SECOUNDS_PARALLEL}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def create_wrk_processes(shared_data, number_client, enpoints):
    """Create one wrk process per endpoint."""
    return [
        Process(
            target=wrk_background_process,
            args=(f"{BACKEND_URL}/{end_point}", end_point, shared_data, number_client),
        )
        for end_point in enpoints
    ]


def run_wrk_sequential(enpoints):
    """Run wrk sequential on all endpoints."""
    sequential_results = {}
    for number_client in NUMBER_CLIENTS:
        sequential_results[number_client] = {}
        for endpoint in enpoints:
            sequential_results[number_client][endpoint] = execute_wrk_on_endpoint(
                f"{BACKEND_URL}/{endpoint}", number_client
            )
    return sequential_results


def run_wrk_parallel(enpoints):
    """Run wrk in parallel on all endpoints."""
    manager = Manager()
    parallel_results = {}
    for number_client in NUMBER_CLIENTS:
        shard_dict = manager.dict()
        processes = create_wrk_processes(shard_dict, number_client, enpoints)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
            process.terminate()
        parallel_results[number_client] = {}
        for key, value in shard_dict.items():
            parallel_results[number_client][key] = value
    return parallel_results


def run_benchmark():
    """Run sequential and parallel wrk benchmark on endpoints."""
    sequential_results = run_wrk_sequential(["manager_metric", "flask_metric"])
    parallel_results = run_wrk_parallel(
        ["manager_time_intense_metric", "manager_metric"]
    )
    print_results(sequential_results, parallel_results, NUMBER_CLIENTS)

    formatted_sequential_results = format_results(sequential_results)
    formatted_parallel_results = format_results(parallel_results)

    path = create_folder("wrk_benchmark")

    plot_theoretical_charts(
        formatted_sequential_results,
        path,
        ("manager_metric", "flask_metric"),
        "theoretical_sequential",
    )
    plot_theoretical_charts(
        formatted_parallel_results,
        path,
        ("manager_metric", "flask_metric"),
        "theoretical_parallel",
    )


if __name__ == "__main__":
    run_benchmark()  # type: ignore
