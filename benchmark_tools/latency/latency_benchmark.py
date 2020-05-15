"""Tool for executing curl on endpoint."""
from statistics import mean, median

from benchmark_tools.latency.curl_wrapper import (
    add_database,
    delete_database,
    execute_get,
    post_sql,
    start_worker,
    start_workload,
    stop_worker,
    stop_workload,
)

RUNS = 100

GET_ENDPOINTS = [
    "workload",
    "database",
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def get_endpoints():
    for enpoint in GET_ENDPOINTS:
        print(f"Run on {enpoint}")
        server_process_times = []
        for _ in range(RUNS):
            results = execute_get(enpoint)
            server_process_times.append(results["total"] - results["pretransfer"])
        print(f"Avg: {mean(server_process_times) * 1_000}ms")
        print(f"Median: {median(server_process_times) * 1_000}ms")


def add_delete_database():
    add_server_process_times = []
    delete_server_process_times = []
    for _ in range(RUNS):
        add_result = add_database("db")
        add_server_process_times.append(add_result["total"] - add_result["pretransfer"])
        delete_result = delete_database("db")
        delete_server_process_times.append(
            delete_result["total"] - delete_result["pretransfer"]
        )

    print("Run add database")
    print(f"Avg: {mean(add_server_process_times) * 1_000}ms")
    print(f"Median: {median(add_server_process_times) * 1_000}ms")

    print("Run delete database")
    print(f"Avg: {mean(delete_server_process_times) * 1_000}ms")
    print(f"Median: {median(delete_server_process_times) * 1_000}ms")


def start_stop_worker():
    add_database("db")
    start_server_process_times = []
    stop_server_process_times = []
    for _ in range(RUNS):
        start_result = start_worker()
        start_server_process_times.append(
            start_result["total"] - start_result["pretransfer"]
        )
        stop_result = stop_worker()
        stop_server_process_times.append(
            stop_result["total"] - stop_result["pretransfer"]
        )
    delete_database("db")

    print("Run start worker")
    print(f"Avg: {mean(start_server_process_times) * 1_000}ms")
    print(f"Median: {median(start_server_process_times) * 1_000}ms")

    print("Run stop worker")
    print(f"Avg: {mean(stop_server_process_times) * 1_000}ms")
    print(f"Median: {median(stop_server_process_times) * 1_000}ms")


def start_stop_workload():
    start_server_process_times = []
    stop_server_process_times = []
    for _ in range(RUNS):
        start_result = start_workload()
        start_server_process_times.append(
            start_result["total"] - start_result["pretransfer"]
        )
        stop_result = stop_workload()
        stop_server_process_times.append(
            stop_result["total"] - stop_result["pretransfer"]
        )

    print("Run start workload")
    print(f"Avg: {mean(start_server_process_times) * 1_000}ms")
    print(f"Median: {median(start_server_process_times) * 1_000}ms")

    print("Run stop workload")
    print(f"Avg: {mean(stop_server_process_times) * 1_000}ms")
    print(f"Median: {median(stop_server_process_times) * 1_000}ms")


def execute_sql():
    add_database("db")
    server_process_times = []
    for _ in range(RUNS):
        result = post_sql("db")
        server_process_times.append(result["total"] - result["pretransfer"])
    print("Run execute sql")
    print(f"Avg: {mean(server_process_times) * 1_000}ms")
    print(f"Median: {median(server_process_times) * 1_000}ms")

    delete_database("db")


def run_benchmark():
    """Run benchmark."""
    get_endpoints()
    add_delete_database()
    start_stop_worker()
    start_stop_workload()
    execute_sql()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
