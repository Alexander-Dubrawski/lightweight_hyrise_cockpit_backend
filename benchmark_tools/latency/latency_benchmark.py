"""Tool for executing curl on endpoint."""

from benchmark_tools.graph_plotter import plot_avg_med_bar_chart
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
from benchmark_tools.latency.print_data import print_data

RUNS = 10

GET_ENDPOINTS = [
    "workload",
    "database",
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def get_endpoints():
    enpoint_results = {}
    for endpoint in GET_ENDPOINTS:
        server_process_times = []
        name_lookup_times = []
        connect_times = []
        for _ in range(RUNS):
            results = execute_get(endpoint)
            server_process_times.append(results["total"] - results["pretransfer"])
            name_lookup_times.append(results["namelookup"])
            connect_times.append(results["connect"] - results["namelookup"])
        enpoint_results[endpoint] = {
            "server_process_times": server_process_times,
            "name_lookup_times": name_lookup_times,
            "connect_times": connect_times,
        }
    return enpoint_results


def post_delete_on_endpoint(
    endpoint, post_endpoint_handler, delete_enpoint_handler, handler_argument=None
):
    post_to_server_process_times = []
    post_to_name_lookup_times = []
    post_to_connect_times = []
    delete_to_server_process_times = []
    delete_to_name_lookup_times = []
    delete_to_connect_times = []

    for _ in range(RUNS):
        if handler_argument:
            post_result = post_endpoint_handler(handler_argument)
        else:
            post_result = post_endpoint_handler()
        post_to_server_process_times.append(
            post_result["total"] - post_result["pretransfer"]
        )
        post_to_name_lookup_times.append(post_result["namelookup"])
        post_to_connect_times.append(post_result["connect"] - post_result["namelookup"])
        if handler_argument:
            delete_result = delete_enpoint_handler(handler_argument)
        else:
            delete_result = delete_enpoint_handler()
        delete_to_server_process_times.append(
            delete_result["total"] - delete_result["pretransfer"]
        )
        delete_to_name_lookup_times.append(delete_result["namelookup"])
        delete_to_connect_times.append(
            delete_result["connect"] - delete_result["namelookup"]
        )

    return {
        f"Post {endpoint}": {
            "server_process_times": post_to_server_process_times,
            "name_lookup_times": post_to_name_lookup_times,
            "connect_times": post_to_connect_times,
        },
        f"Delete {endpoint}": {
            "server_process_times": delete_to_server_process_times,
            "name_lookup_times": delete_to_name_lookup_times,
            "connect_times": delete_to_connect_times,
        },
    }


def execute_sql():
    add_database("db")
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    for _ in range(RUNS):
        results = post_sql("db")
        server_process_times.append(results["total"] - results["pretransfer"])
        name_lookup_times.append(results["namelookup"])
        connect_times.append(results["connect"] - results["namelookup"])

    delete_database("db")

    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def get_enpoint_request():
    results = get_endpoints()
    for endpoint, result in results.items():
        print_data(endpoint, result)
    plot_avg_med_bar_chart(results, "latency_get_endpoints", "server_process_times")


def add_delete_database():
    result = post_delete_on_endpoint("Database", add_database, delete_database, "db")
    print_data("Add Database", result["Post Database"])
    print_data("Delete Database", result["Delete Database"])


def start_stop_worker():
    result = post_delete_on_endpoint("Worker", start_worker, stop_worker)
    print_data("Start Worker", result["Post Worker"])
    print_data("Stop Worker", result["Delete Worker"])


def start_stop_workload():
    result = post_delete_on_endpoint("Workload", start_workload, stop_workload)
    print_data("Start Workload", result["Post Workload"])
    print_data("Stop Workload", result["Delete Workload"])


def post_to_sql_endpoint():
    result = execute_sql()
    print_data("Execute sql", result)


def run_benchmark():
    """Run benchmark."""
    get_enpoint_request()
    add_delete_database()
    start_stop_worker()
    start_stop_workload()
    execute_sql()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
