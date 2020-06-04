from calendar import timegm
from datetime import datetime
from json import loads
from os import mkdir
from time import gmtime

from .graph_plotter import plot_bar_chart_for_endpoint, plot_hdr_histogram_for_endpoint


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


def print_results(sequential_results, parallel_results, number_clients):
    """Print wrk output directly to terminal."""
    print_cyan("\nResults for sequential wrk")
    print_output(sequential_results, number_clients)
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


def plot_theoretical_charts(data, path, endpoints, filename):
    plot_bar_chart_for_endpoint(
        data,
        path,
        "Req/Sec",
        f"bar_{filename}_throughput",
        "req/sec",
        endpoints,
        "number of clients",
    )
    plot_hdr_histogram_for_endpoint(data, path, f"hdr_{filename}_throughput")
