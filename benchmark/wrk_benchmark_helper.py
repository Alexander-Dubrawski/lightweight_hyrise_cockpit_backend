from calendar import timegm
from datetime import datetime
from json import loads
from os import mkdir
from time import gmtime

from requests import delete, post

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .graph_plotter import (
    plot_bar_chart_for_endpoint,
    plot_hdr_histogram_for_endpoint,
    plot_hdr_histogram_for_single_endpoint,
    plot_hdr_historgram_for_system_data,
)

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"


def add_database(database_id: str):
    """Add database."""
    body = {
        "id": database_id,
        "number_workers": 4,
    }
    url = f"{BACKEND_URL}/database"
    return post(url, json=body)


def remove_database(database_id: str):
    """Remove database."""
    body = {"id": database_id}
    url = f"{BACKEND_URL}/database"
    return delete(url, json=body)


def start_workload():
    """Start workload execution."""
    body = {"workload_name": "fake_workload", "frequency": 10000}
    url = f"{BACKEND_URL}/workload"
    return post(url, json=body)


def stop_workload():
    """Stop workload execution."""
    url = f"{BACKEND_URL}/workload"
    return delete(url)


def start_workers():
    """Start worker pool."""
    url = f"{BACKEND_URL}/worker"
    return post(url)


def stop_workers():
    """Stop worker pool."""
    url = f"{BACKEND_URL}/worker"
    return delete(url)


def format_results(results):
    """Extract Requests/sec and Latency from wrk output and saves it in a dictionary structure."""
    formatted_results = {}
    for number_clients, value in results.items():
        formatted_results[number_clients] = {}
        for endpoint, output in value.items():
            split_output = output.splitlines()
            index_latency_values = split_output.index("latency_values:")
            index_request_values = split_output.index("request_values:")
            index_latency_distribution = split_output.index("latency_distribution:")
            index_percentiles = split_output.index("percentiles:")
            formatted_results[number_clients][endpoint] = {
                "Latency": loads(split_output[index_latency_values + 1]),
                "latency_distribution": loads(
                    split_output[index_latency_distribution + 1]
                ),
                "Req/Sec": loads(split_output[index_request_values + 1]),
                "latency_percentiles": loads(split_output[index_percentiles + 1]),
            }
    return formatted_results


def print_cyan(value):
    """Print cyan colored text."""
    print("\033[96m{}\033[00m".format(value))


def print_purple(value):
    """Print purple colored text."""
    print("\033[94m{}\033[00m".format(value))


def print_output(results, number_clients):
    """Print results of benchmark."""
    for number_client, value in results.items():
        print_purple(f"\nNumber clients: {number_client}")
        for output in value.values():
            print(output)


def print_user_results(results):
    """Print wrk output directly to terminal."""
    print_cyan("\nResults for user scenario wrk")
    print_output(results, [1])


def print_results(sequential_results, parallel_results, number_clients):
    """Print wrk output directly to terminal."""
    print_cyan("\nResults for sequential wrk")
    print_output(sequential_results, number_clients)
    if parallel_results:
        print_cyan("\nResults for parallel wrk")
        print_output(parallel_results, number_clients)


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    mkdir(f"{path}/theoretical_sequential")
    mkdir(f"{path}/theoretical_parallel")
    mkdir(f"{path}/user_parallel")
    return path


def plot_charts(data, path, endpoints, filename, x_label):
    plot_bar_chart_for_endpoint(
        data,
        path,
        "Req/Sec",
        f"bar_{filename}_throughput",
        "req/sec",
        endpoints,
        x_label,
    )
    plot_hdr_histogram_for_endpoint(data, path, f"hdr_{filename}_throughput", x_label)
    endpoint_one, endpoint_two = endpoints
    plot_hdr_histogram_for_single_endpoint(
        data, path, f"hdr_{endpoint_one}_{filename}_throughput", x_label, endpoint_one
    )
    plot_hdr_histogram_for_single_endpoint(
        data, path, f"hdr_{endpoint_two}_{filename}_throughput", x_label, endpoint_two
    )


def plot_system_data(data, path, duration, metric):
    plot_hdr_historgram_for_system_data(data, path, duration, metric)
