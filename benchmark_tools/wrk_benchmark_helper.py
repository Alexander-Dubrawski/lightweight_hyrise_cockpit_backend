from calendar import timegm
from csv import writer
from datetime import datetime
from json import loads
from os import mkdir
from re import findall
from time import gmtime

from requests import delete, post

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .graph_plotter import (
    plot_bar_chart,
    plot_comparison_parallel_sequential,
    plot_hdr_histogram,
)

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"


def print_cyan(value):
    """Print cyan colored text."""
    print("\033[96m{}\033[00m".format(value))


def add_database(database_id: str):
    """Add database."""
    body = {
        "id": database_id,
        "host": "host",
        "port": "port",
        "number_workers": 10,
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


def get_usage_in_ms(usage):
    """Convert time entity to ms."""
    m_metric_converter = {
        "us": lambda m: m / 1_000,
        "ms": lambda m: m,
        "s": lambda m: m / 1_000,
        "m": lambda m: m * 60_000,
    }
    usage_number = findall(r"[-+]?\d*\.\d+|\d+", usage)[0]
    metric = list(filter(None, findall(r"[a-z]*", usage)))[0]
    return m_metric_converter[metric](float(usage_number))


def format_results(results):
    """Extract Requests/sec and Latency from wrk output and saves it in a dictionary structure."""
    formatted_results = {}
    for endpoint, output in results.items():
        split_output = output.splitlines()
        index_latency_values = split_output.index("latency_values:")
        index_request_values = split_output.index("request_values:")
        index_latency_distribution = split_output.index("latency_distribution:")
        index_percentiles = split_output.index("percentiles:")
        formatted_results[endpoint] = {
            "Latency": loads(split_output[index_latency_values + 1]),
            "latency_distribution": loads(split_output[index_latency_distribution + 1]),
            "Req/Sec": loads(split_output[index_request_values + 1]),
            "latency_percentiles": loads(split_output[index_percentiles + 1]),
        }
    return formatted_results


def print_output(results):
    """Print results of benchmark."""
    for output in results.values():
        print(output)


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    mkdir(f"{path}/hdr_histogram")
    mkdir(f"{path}/bar_charts")
    return path


def write_to_csv(sequential_data, parallel_data, path):
    """Write benchmark results to CSV file."""
    with open(f"{path}/wrk_throughput.csv", "w", newline="") as f:
        filednames = ["Endpoints", "Avg", "Stdev", "Max", "Mode"]
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        sequential_rows = [
            [
                endpoint,
                results["Req/Sec"]["Avg"],
                results["Req/Sec"]["Stdev"],
                results["Req/Sec"]["Max"],
                "sequential",
            ]
            for endpoint, results in sequential_data.items()
        ]
        parallel_rows = [
            [
                endpoint,
                results["Req/Sec"]["Avg"],
                results["Req/Sec"]["Stdev"],
                results["Req/Sec"]["Max"],
                "parallel",
            ]
            for endpoint, results in parallel_data.items()
        ]
        csv_writer.writerows(sequential_rows)
        csv_writer.writerows(parallel_rows)
    with open(f"{path}/wrk_latency.csv", "w", newline="") as f:
        filednames = [
            "Endpoints",
            "Avg",
            "Stdev",
            "Max",
            "LD_25%",
            "LD_50%",
            "LD_75%",
            "LD_90%",
            "LD_99%",
            "LD_99.9%",
            "LD_99.99%",
            "LD_99.999%",
            "LD_100%",
            "Mode",
        ]
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        sequential_rows = [
            [
                endpoint,
                results["Latency"]["Avg"],
                results["Latency"]["Stdev"],
                results["Latency"]["Max"],
                results["latency_distribution"]["25%"],
                results["latency_distribution"]["50%"],
                results["latency_distribution"]["75%"],
                results["latency_distribution"]["90%"],
                results["latency_distribution"]["99%"],
                results["latency_distribution"]["99.9%"],
                results["latency_distribution"]["99.99%"],
                results["latency_distribution"]["99.999%"],
                results["latency_distribution"]["100%"],
                "sequential",
            ]
            for endpoint, results in sequential_data.items()
        ]
        parallel_rows = [
            [
                endpoint,
                results["Latency"]["Avg"],
                results["Latency"]["Stdev"],
                results["Latency"]["Max"],
                results["latency_distribution"]["25%"],
                results["latency_distribution"]["50%"],
                results["latency_distribution"]["75%"],
                results["latency_distribution"]["90%"],
                results["latency_distribution"]["99%"],
                results["latency_distribution"]["99.9%"],
                results["latency_distribution"]["99.99%"],
                results["latency_distribution"]["99.999%"],
                results["latency_distribution"]["100%"],
                "parallel",
            ]
            for endpoint, results in parallel_data.items()
        ]
        csv_writer.writerows(sequential_rows)
        csv_writer.writerows(parallel_rows)
    with open(f"{path}/wrk_percentiles_latency.csv", "w", newline="") as f:
        endpoints = sequential_data.keys()
        filednames = ["percentile"]
        for endpoint in endpoints:
            filednames.append(f"{endpoint}_sequencial")
        for endpoint in endpoints:
            filednames.append(f"{endpoint}_parallel")
        rows = []
        for i in range(100):
            row = [i + 1]
            row += [
                sequential_data[endpoint]["latency_percentiles"]["percentiles"][i]
                for endpoint in endpoints
            ]
            row += [
                parallel_data[endpoint]["latency_percentiles"]["percentiles"][i]
                for endpoint in endpoints
            ]
            rows.append(row)
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        csv_writer.writerows(rows)


def plot_results(path, formatted_sequential_results, formatted_parallel_results):
    """Plots wrk results in bar charts."""
    path_bar_chart = f"{path}/bar_charts"
    plot_bar_chart(
        formatted_sequential_results,
        path_bar_chart,
        "Latency",
        "sequenzial_latency",
        "Latency in ms",
    )
    plot_bar_chart(
        formatted_parallel_results,
        path_bar_chart,
        "Latency",
        "parallel_latency",
        "Latency in ms",
    )
    plot_bar_chart(
        formatted_sequential_results,
        path_bar_chart,
        "Req/Sec",
        "sequenzial_throughput",
        "Throughput in req/sec",
    )
    plot_bar_chart(
        formatted_parallel_results,
        path_bar_chart,
        "Req/Sec",
        "parallel_throughput",
        "Throughput in req/sec",
    )
    plot_comparison_parallel_sequential(
        formatted_sequential_results,
        formatted_parallel_results,
        path_bar_chart,
        "Latency",
        "Avg",
        "comparison_latency",
        "Latency in ms",
    )
    plot_comparison_parallel_sequential(
        formatted_sequential_results,
        formatted_parallel_results,
        path_bar_chart,
        "Req/Sec",
        "Avg",
        "comparison_throughput",
        "Throughput in req/sec",
    )
    hdr_historgam_path = f"{path}/hdr_histogram"
    plot_hdr_histogram(
        formatted_sequential_results,
        hdr_historgam_path,
        "HdrHistogramm_comparison_sequential",
    )
    plot_hdr_histogram(
        formatted_parallel_results,
        hdr_historgam_path,
        "HdrHistogramm_comparison_parallel",
    )
    endpoints = formatted_sequential_results.keys()
    for endpoint in endpoints:
        data = {
            f"{endpoint}_sequencial": formatted_sequential_results[endpoint],
            f"{endpoint}_parallel": formatted_parallel_results[endpoint],
        }
        plot_hdr_histogram(
            data,
            hdr_historgam_path,
            f"{endpoint}_HdrHistogramm_comparison_sequential_parallel",
        )
    comparison_sequential_parallel = {}
    for endpoint in endpoints:
        comparison_sequential_parallel[
            f"{endpoint}_sequencial"
        ] = formatted_sequential_results[endpoint]
        comparison_sequential_parallel[
            f"{endpoint}_parallel"
        ] = formatted_parallel_results[endpoint]
    plot_hdr_histogram(
        comparison_sequential_parallel,
        hdr_historgam_path,
        "HdrHistogramm_comparison_parallel_and_sequential",
    )


def print_results(sequential_results, parallel_results):
    """Print wrk output directly to terminal."""
    print_cyan("\nResults for sequential wrk")
    print_output(sequential_results)
    print_cyan("\nResults for parallel wrk")
    print_output(parallel_results)
