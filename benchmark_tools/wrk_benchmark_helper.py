from calendar import timegm
from csv import writer
from datetime import datetime
from os import mkdir
from re import findall
from time import gmtime

from requests import delete, post

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .graph_plotter import plot_bar_chart, plot_comparison_parallel_sequential

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
        output_split = output.split()
        index_latency = output_split.index("Latency")
        index_latency_distribution = output_split.index("Distribution")
        index_req_sec = output_split.index("Req/Sec")
        formatted_results[endpoint] = {
            "Latency": {
                "Avg": get_usage_in_ms(output_split[index_latency + 1]),
                "Stdev": get_usage_in_ms(output_split[index_latency + 2]),
                "Max": get_usage_in_ms(output_split[index_latency + 3]),
                "+/- Stdev in %": float(
                    findall(r"[-+]?\d*\.\d+|\d+", output_split[index_latency + 4])[0]
                ),
                "distribution": {
                    "50%": get_usage_in_ms(
                        output_split[index_latency_distribution + 2]
                    ),
                    "75%": get_usage_in_ms(
                        output_split[index_latency_distribution + 4]
                    ),
                    "90%": get_usage_in_ms(
                        output_split[index_latency_distribution + 6]
                    ),
                    "99%": get_usage_in_ms(
                        output_split[index_latency_distribution + 8]
                    ),
                },
            },
            "Req/Sec": {
                "Avg": float(output_split[index_req_sec + 1]),
                "Stdev": float(output_split[index_req_sec + 2]),
                "Max": float(output_split[index_req_sec + 3]),
                "+/- Stdev in %": float(
                    findall(r"[-+]?\d*\.\d+|\d+", output_split[index_req_sec + 4])[0]
                ),
            },
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
    return path


def write_to_csv(sequential_data, parallel_data, path):
    """Write benchmark results to CSV file."""
    with open(f"{path}/wrk_throughput.csv", "w", newline="") as f:
        filednames = ["Endpoints", "Avg", "Stdev", "Max", "+/- Stdev in %", "Mode"]
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        sequential_rows = [
            [
                endpoint,
                results["Req/Sec"]["Avg"],
                results["Req/Sec"]["Stdev"],
                results["Req/Sec"]["Max"],
                results["Req/Sec"]["+/- Stdev in %"],
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
                results["Req/Sec"]["+/- Stdev in %"],
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
            "+/- Stdev in %",
            "LD_50%",
            "LD_75%",
            "LD_90%",
            "LD_99%",
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
                results["Latency"]["+/- Stdev in %"],
                results["Latency"]["distribution"]["50%"],
                results["Latency"]["distribution"]["75%"],
                results["Latency"]["distribution"]["90%"],
                results["Latency"]["distribution"]["99%"],
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
                results["Latency"]["+/- Stdev in %"],
                results["Latency"]["distribution"]["50%"],
                results["Latency"]["distribution"]["75%"],
                results["Latency"]["distribution"]["90%"],
                results["Latency"]["distribution"]["99%"],
                "parallel",
            ]
            for endpoint, results in parallel_data.items()
        ]
        csv_writer.writerows(sequential_rows)
        csv_writer.writerows(parallel_rows)


def plot_results(path, formatted_sequential_results, formatted_parallel_results):
    """Plots wrk results in bar charts."""
    plot_bar_chart(
        formatted_sequential_results,
        path,
        "Latency",
        "sequenzial_latency",
        "Latency in ms",
    )
    plot_bar_chart(
        formatted_parallel_results, path, "Latency", "parallel_latency", "Latency in ms"
    )
    plot_bar_chart(
        formatted_sequential_results,
        path,
        "Req/Sec",
        "sequenzial_throughput",
        "Throughput in req/sec",
    )
    plot_bar_chart(
        formatted_parallel_results,
        path,
        "Req/Sec",
        "parallel_throughput",
        "Throughput in req/sec",
    )
    plot_comparison_parallel_sequential(
        formatted_sequential_results,
        formatted_parallel_results,
        path,
        "Latency",
        "Avg",
        "comparison_latency",
        "Latency in ms",
    )
    plot_comparison_parallel_sequential(
        formatted_sequential_results,
        formatted_parallel_results,
        path,
        "Req/Sec",
        "Avg",
        "comparison_throughput",
        "Throughput in req/sec",
    )


def print_results(sequential_results, parallel_results):
    """Print wrk output directly to terminal."""
    print_cyan("\nResults for sequential wrk")
    print_output(sequential_results)
    print_cyan("\nResults for parallel wrk")
    print_output(parallel_results)
