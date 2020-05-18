"""Tool for executing curl on endpoint."""
from calendar import timegm
from csv import writer
from datetime import datetime
from os import mkdir
from statistics import mean, median
from time import gmtime

from benchmark_tools.graph_plotter import (
    plot_avg_med_bar_chart,
    plot_bar_chart,
    plot_stacked_bar_chart,
)
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

RUNS = 20

MONITOR_ENDPOINTS = [
    "workload",
    "database",
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def get_on_endpoints():
    """
    Fetch data from endpoint.

    Use curl wrapper to fetch data from all MONITOR_ENDPOINTS and calculate latencies.

    Returns:
        Dictionary:
            server_process_times: Time it took to process request in server.
            name_lookup_times: name lookup time.
            connect_times: time it took to connect to server.
    """
    enpoint_results = {}
    for endpoint in MONITOR_ENDPOINTS:
        server_process_times = []
        name_lookup_times = []
        connect_times = []
        for _ in range(RUNS):
            results = execute_get(endpoint)
            server_process_times.append(results["total"] - results["pretransfer"])
            name_lookup_times.append(results["namelookup"])
            connect_times.append(results["connect"] - results["namelookup"])
        enpoint_results[f"GET {endpoint}"] = {
            "server_process_times": server_process_times,
            "name_lookup_times": name_lookup_times,
            "connect_times": connect_times,
        }
    return enpoint_results


def post_delete_on_endpoint(
    endpoint, post_endpoint_handler, delete_enpoint_handler, handler_argument=None
):
    """
    Alternately execute POST and then DELETE on endpoint.

    For every run first use curl wrapper for POST and then DELETE for the same endpoint.
    """
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
        f"POST {endpoint}": {
            "server_process_times": post_to_server_process_times,
            "name_lookup_times": post_to_name_lookup_times,
            "connect_times": post_to_connect_times,
        },
        f"DELETE {endpoint}": {
            "server_process_times": delete_to_server_process_times,
            "name_lookup_times": delete_to_name_lookup_times,
            "connect_times": delete_to_connect_times,
        },
    }


def post_on_sql_endpoint():
    """
    POST to SQL endpoint.

    First use POST to add a database, then execute POST to SQL Endpoint, after that remove database.
    """
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


def benchmark_get_endpoints():
    """Execute benchmark on MONITORE_ENDPOINTS."""
    results = get_on_endpoints()
    for endpoint, result in results.items():
        print_data(endpoint, result)
    return results


def benchmark_database_endpoint():
    """Execute benchmark on add and delete database."""
    result = post_delete_on_endpoint("Database", add_database, delete_database, "db")
    print_data("POST Database", result["POST Database"])
    print_data("DELETE Database", result["DELETE Database"])
    return result


def benchmark_worker_endpoint():
    """Execute benchmark on start and stop worker."""
    result = post_delete_on_endpoint("Worker", start_worker, stop_worker)
    print_data("POST Worker", result["POST Worker"])
    print_data("DELETE Worker", result["DELETE Worker"])
    return result


def benchmark_workload_endpoint():
    """Execute benchmark on start and stop workload."""
    result = post_delete_on_endpoint("Workload", start_workload, stop_workload)
    print_data("POST Workload", result["POST Workload"])
    print_data("DELETE Workload", result["DELETE Workload"])
    return result


def benchmark_sql_endpoint():
    """Execute benchmark on execute SQL query."""
    result = post_on_sql_endpoint()
    print_data("POST sql", result)
    return result


def create_folder():
    """
    Create folder to save benchmark results.

    Create Latency folder and append UNIX time stamp to it.
    """
    ts = timegm(gmtime())
    path = f"measurements/Latency_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    mkdir(f"{path}/server_process_times")
    mkdir(f"{path}/name_lookup_times")
    mkdir(f"{path}/connect_times")
    mkdir(f"{path}/stacked")
    return path


def write_to_csv(data, path):
    """
    Write benchmark results to CSV file.

    Create for all the latency intervals a separate CSV file.
    """
    latency_types = ["server_process_times", "name_lookup_times", "connect_times"]
    for latency_type in latency_types:
        with open(f"{path}/{latency_type}/{latency_type}.csv", "w", newline="") as f:
            endpoints = list(data.keys())
            filednames = list(data.keys())
            filednames.insert(0, "run")
            csv_writer = writer(f, delimiter="|")
            csv_writer.writerow(filednames)
            rows = []
            for i in range(RUNS):
                row = []
                row.append(i)
                for endpoint in endpoints:
                    row.append(data[endpoint][latency_type][i])
                rows.append(row)
            csv_writer.writerows(rows)


def run_benchmark():
    """
    Run benchmark.

    Execute benchmark on all endpoints than plot graphs and create CSV.
    """
    results_get_endpoints = benchmark_get_endpoints()
    results_database_endpoint = benchmark_database_endpoint()
    results_worker_endpoint = benchmark_worker_endpoint()
    results_workload_endpoint = benchmark_workload_endpoint()
    results_sql_endpoint = benchmark_sql_endpoint()

    main_path = create_folder()

    results = {
        **results_get_endpoints,
        **results_database_endpoint,
        **results_worker_endpoint,
        **results_workload_endpoint,
        **{"POST sql": {**results_sql_endpoint}},
    }

    latency_types = ["server_process_times", "name_lookup_times", "connect_times"]

    for latency_type in latency_types:
        path = f"{main_path}/{latency_type}"
        plot_avg_med_bar_chart(
            results_get_endpoints,
            path,
            f"{latency_type}_latency_get_endpoints",
            latency_type,
        )
        plot_avg_med_bar_chart(
            results_database_endpoint,
            path,
            f"{latency_type}_latency_post_delete_database",
            latency_type,
        )
        plot_avg_med_bar_chart(
            results_worker_endpoint,
            path,
            f"{latency_type}_latency_post_delete_worker",
            latency_type,
        )
        plot_avg_med_bar_chart(
            results_workload_endpoint,
            path,
            f"{latency_type}_latency_post_delete_workload",
            latency_type,
        )
        plot_avg_med_bar_chart(
            {"sql": results_sql_endpoint},
            path,
            f"{latency_type}_latency_post_sql",
            latency_type,
        )
        plot_bar_chart(
            results, path, f"avg_{latency_type}_latency", latency_type, mean, "AVG"
        )
        plot_bar_chart(
            results, path, f"med_{latency_type}_latency", latency_type, median, "MED"
        )

    plot_stacked_bar_chart(
        results, f"{main_path}/stacked", "med_latency_distribution", median
    )
    plot_stacked_bar_chart(
        results, f"{main_path}/stacked", "avg_latency_distribution", mean
    )
    write_to_csv(results, main_path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
