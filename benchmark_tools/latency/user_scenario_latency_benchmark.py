"""Tool for executing user scenario latency benchmark."""
from multiprocessing import Manager, Process

from benchmark_tools.graph_plotter import plot_line_chart_avg_med
from benchmark_tools.latency.curl_wrapper import (
    add_database,
    delete_database,
    execute_get,
    start_worker,
    start_workload,
    stop_worker,
    stop_workload,
)
from benchmark_tools.latency.print_data import print_data

RUNS = 200
NUMBER_DATABASES = 2

GET_ENDPOINTS = [
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def execute_fetch_endpoint(endpoint):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    for _ in range(RUNS):
        results = execute_get(endpoint)
        server_process_times.append(results["total"] - results["pretransfer"])
        name_lookup_times.append(results["namelookup"])
        connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def fetch_endpoints_sequenzial():
    benchamrk_results = {}
    for endpoint in GET_ENDPOINTS:
        benchamrk_results[endpoint] = execute_fetch_endpoint(endpoint)
    return benchamrk_results


def fetch_endpoint(endpoint, shared_data):
    shared_data[endpoint] = execute_fetch_endpoint(endpoint)


def fetch_endpoints_parrallel():
    manager = Manager()
    shared_data = manager.dict()
    processes = [
        Process(target=fetch_endpoint, args=(endpoint, shared_data,))
        for endpoint in GET_ENDPOINTS
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()

    return shared_data


def add_delete_multiple_databases(handler):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    for i in range(NUMBER_DATABASES):
        results = handler(f"db_{i}")
        server_process_times.append(results["total"] - results["pretransfer"])
        name_lookup_times.append(results["namelookup"])
        connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def post_data(handler):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    results = handler()
    server_process_times.append(results["total"] - results["pretransfer"])
    name_lookup_times.append(results["namelookup"])
    connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def run_benchmark():

    result = add_delete_multiple_databases(add_database)
    print_data("Add Database", result)

    result = post_data(start_workload)
    print_data("Start Workload", result)

    result = post_data(start_worker)
    print_data("Start Worker", result)

    results = fetch_endpoints_sequenzial()
    for endpoint, result in results.items():
        print_data(endpoint, result)
    plot_line_chart_avg_med(
        results, "sequenzial_latency", "server_process_times", interpolation_factor=10
    )

    results = fetch_endpoints_parrallel()
    for endpoint, result in results.items():
        print_data(endpoint, result)
    plot_line_chart_avg_med(
        results, "parallel_latency", "server_process_times", interpolation_factor=10
    )

    result = post_data(stop_worker)
    print_data("Stop Worker", result)

    result = post_data(stop_workload)
    print_data("Stop Workload", result)

    result = add_delete_multiple_databases(delete_database)
    print_data("Delete Database", result)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
