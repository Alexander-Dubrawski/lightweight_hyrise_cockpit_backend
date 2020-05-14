"""Tool for executing user scenario latency benchmark."""
from multiprocessing import Process
from statistics import mean, median

from benchmark_tools.latency.curl_wrapper import (
    add_database,
    delete_database,
    execute_get,
    start_worker,
    start_workload,
    stop_worker,
    stop_workload,
)

RUNS = 100
NUMBER_DATABASES = 5

GET_ENDPOINTS = [
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def fetch_endpoint(endpoint):
    server_process_times = []
    for _ in range(RUNS):
        results = execute_get(endpoint)
        server_process_times.append(results["total"] - results["pretransfer"])
    avg = mean(server_process_times) * 1_000
    med = median(server_process_times) * 1_000
    print(f"Run on {endpoint}\nAvg: {avg}\nMedian: {med}")


def fetch_endpoints_parrallel():
    processes = [
        Process(target=fetch_endpoint, args=(endpoint,)) for endpoint in GET_ENDPOINTS
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()


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

    fetch_endpoints_parrallel()

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
