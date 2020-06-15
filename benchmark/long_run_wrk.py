"""Tool for executing wrk benchmark."""
import signal
from json import dumps
from multiprocessing import Process
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .wrk_benchmark_helper import (
    create_folder,
    format_results,
    plot_charts,
    print_results,
    start_manager,
    start_workload_generator,
    start_wsgi_server,
)

NUMBER_CLIENTS = [1, 2, 4, 8, 16, 32, 64]
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_MINUTES = 60
DURATION_IN_SECOUNDS_PARALLEL = 10
ENDPOINTS = ["manager_time_intense_metric", "manager_metric", "flask_metric"]


def execute_wrk_on_endpoint(url, number_clinets):
    """Background process to execute wrk."""
    return check_output(
        f"numactl -m 0 --physcpubind 20-79 wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_MINUTES}m --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def wrk_background_process(url, endpoint, shared_data, number_clinets):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"numactl -m 0 --physcpubind 20-79 wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_SECOUNDS_PARALLEL}s --timeout 10s {url}",
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


def run_wrk_sequential(enpoints, path):
    """Run wrk sequential on all endpoints."""
    sequential_results = {}
    for number_client in NUMBER_CLIENTS:
        sequential_results[number_client] = {}
        for endpoint in enpoints:
            sequential_results[number_client][endpoint] = execute_wrk_on_endpoint(
                f"{BACKEND_URL}/{endpoint}", number_client
            )
            with open(f"{path}/{number_client}_{endpoint}_results.txt", "w+") as file:
                file.write(sequential_results[number_client][endpoint])
    return sequential_results


def run_benchmark():
    """Run sequential and parallel wrk benchmark on endpoints."""
    path = create_folder("wrk_benchmark")
    server = start_wsgi_server(1, 1)
    manager = start_manager()
    generator = start_workload_generator()
    sequential_results = run_wrk_sequential(["manager_metric", "flask_metric"], path)
    print_results(sequential_results, None, NUMBER_CLIENTS)
    formatted_sequential_results = format_results(sequential_results)

    with open(f"{path}/formatted_sequential_results.txt", "+w") as file:
        file.write(dumps(formatted_sequential_results))

    server.send_signal(signal.SIGINT)
    server.wait()
    manager.send_signal(signal.SIGINT)
    manager.wait()
    generator.send_signal(signal.SIGINT)
    generator.wait()

    plot_charts(
        formatted_sequential_results,
        path,
        ("manager_metric", "flask_metric"),
        "theoretical_sequential",
        "client",
    )


if __name__ == "__main__":
    run_benchmark()  # type: ignore
