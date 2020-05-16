"""Tool for executing wrk benchmark in multiple processes."""

from calendar import timegm
from csv import writer
from datetime import datetime
from multiprocessing import Manager, Process
from os import mkdir
from subprocess import check_output
from time import gmtime

from benchmark_tools.graph_plotter import plot_bar_chart_throughput
from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 10
ENDPOINTS = ["workload", "database", "queue_length", "storage", "throughput", "latency"]


def wrk_background_process(url, endpoint, shared_data):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"wrk -t1 -c1 -d{DURATION_IN_SECOUNDS}s {url}", shell=True
    ).decode("utf-8")


def create_wrk_processes(shared_data):
    """Create one wrk process per endpoint."""
    return [
        Process(
            target=wrk_background_process,
            args=(f"{BACKEND_URL}/{end_point}", end_point, shared_data),
        )
        for end_point in ENDPOINTS
    ]


def get_format_results(results):
    formatted_results = {}
    for endpoint, output in results.items():
        output_split = output.split()
        formatted_results[endpoint] = output_split[
            output_split.index("Requests/sec:") + 1
        ]
    return formatted_results


def print_output(results):
    for output in results.values():
        print(output)


def create_folder():
    ts = timegm(gmtime())
    path = f"measurements/Throughput_parallel_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def write_to_csv(data, path):
    with open(f"{path}/parallel_throughput.csv", "w", newline="") as f:
        filednames = ["endpoints", "throughput_per_sec"]
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        rows = [[endpoint, throughput] for endpoint, throughput in data.items()]
        csv_writer.writerows(rows)


def run_benchmark():
    """Run wrk benchmark on endpoints."""
    manager = Manager()
    shared_data = manager.dict()
    processes = create_wrk_processes(shared_data)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()

    print_output(shared_data)
    formatted_reults = get_format_results(shared_data)
    path = create_folder()
    plot_bar_chart_throughput(formatted_reults, path, "throughput_comparison")
    write_to_csv(formatted_reults, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
