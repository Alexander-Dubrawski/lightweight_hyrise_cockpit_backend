"""Tool for executing user scenario latency benchmark."""
from multiprocessing import Manager, Process
from statistics import mean, median

from benchmark_tools.graph_plotter import plot_line_chart
from benchmark_tools.latency.curl_wrapper import (
    add_database,
    delete_database,
    execute_get,
    start_worker,
    start_workload,
    stop_worker,
    stop_workload,
)

RUNS = 1000
NUMBER_DATABASES = 5

GET_ENDPOINTS = [
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def fetch_endpoints_sequenzial():
    benchamrk_results = {}
    for endpoint in GET_ENDPOINTS:
        print(f"Run on {endpoint}")
        server_process_times = []
        for _ in range(RUNS):
            results = execute_get(endpoint)
            server_process_times.append(results["total"] - results["pretransfer"])
        benchamrk_results[endpoint] = server_process_times
        print(f"Avg: {mean(server_process_times) * 1_000}ms")
        print(f"Median: {median(server_process_times) * 1_000}ms")
    return benchamrk_results


def fetch_endpoint(endpoint, shared_data):
    server_process_times = []
    for _ in range(RUNS):
        results = execute_get(endpoint)
        server_process_times.append(results["total"] - results["pretransfer"])
    shared_data[endpoint] = server_process_times
    avg = mean(server_process_times) * 1_000
    med = median(server_process_times) * 1_000
    print(f"Run on {endpoint}\nAvg: {avg}\nMedian: {med}")


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


def run_benchmark():

    add_server_process_times = []
    for i in range(NUMBER_DATABASES):
        add_result = add_database(f"db_{i}")
        add_server_process_times.append(add_result["total"] - add_result["pretransfer"])
    print("Add database")
    print(f"Avg: {mean(add_server_process_times) * 1_000}ms")
    print(f"Median: {median(add_server_process_times) * 1_000}ms")

    result = start_workload()
    print("Run start workload")
    print(f"Latency: {(result['total'] - result['pretransfer']) * 1_000}ms")

    result = start_worker()
    print("Run start worker")
    print(f"Latency: {(result['total'] - result['pretransfer']) * 1_000}ms")

    plot_line_chart(fetch_endpoints_sequenzial(), "Latency_squenzial")
    plot_line_chart(fetch_endpoints_parrallel(), "Latency_parallel")

    result = stop_worker()
    print("Run stop worker")
    print(f"Latency: {(result['total'] - result['pretransfer']) * 1_000}ms")

    result = stop_workload()
    print("Run stop workload")
    print(f"Latency: {(result['total'] - result['pretransfer']) * 1_000}ms")

    delete_server_process_times = []
    for i in range(NUMBER_DATABASES):
        delete_result = delete_database(f"db_{i}")
        delete_server_process_times.append(
            delete_result["total"] - delete_result["pretransfer"]
        )
    print("Delete database")
    print(f"Avg: {mean(delete_server_process_times) * 1_000}ms")
    print(f"Median: {median(delete_server_process_times) * 1_000}ms")


if __name__ == "__main__":
    run_benchmark()  # type: ignore
