"""Tool for executing scenario benchmark."""
from calendar import timegm
from csv import writer
from datetime import datetime
from multiprocessing import Manager, Process
from os import mkdir
from subprocess import check_output
from time import gmtime

from requests import delete, post

from benchmark_tools.graph_plotter import plot_bar_chart_throughput
from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
NUMBER_DATABASES = 10
DURATION_IN_SECOUNDS = 30
ENDPOINTS = ["workload", "database", "queue_length", "storage", "throughput", "latency"]


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
    """Extract Requests/sec from wrk output."""
    formatted_results = {}
    for endpoint, output in results.items():
        output_split = output.split()
        formatted_results[endpoint] = output_split[
            output_split.index("Requests/sec:") + 1
        ]
    return formatted_results


def print_output(results):
    """Print results of benchmark."""
    for output in results.values():
        print(output)


def create_folder():
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/Throughput_user_scenario_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def write_to_csv(data, path):
    """Write benchmark results to CSV file."""
    with open(f"{path}/parallel_throughput.csv", "w", newline="") as f:
        filednames = ["endpoints", "throughput_per_sec"]
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        rows = [[endpoint, throughput] for endpoint, throughput in data.items()]
        csv_writer.writerows(rows)


def run_wrk_benchmark(shared_data):
    """Run wrk benchmark on endpoints."""
    processes = create_wrk_processes(shared_data)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()


def run_benchmark():
    """Execute user scenario steps"""
    manager = Manager()
    shared_data = manager.dict()
    total_response_time = 0
    for i in range(NUMBER_DATABASES):
        response = add_database(str(i))
        total_response_time = total_response_time + response.elapsed.total_seconds()
    print(f"\nAvg time to add database: {total_response_time / NUMBER_DATABASES}\n")

    response = start_workload()
    print(f"Time to start workload: {response.elapsed.total_seconds()}\n")

    response = start_workers()
    print(f"Time to start workers: {response.elapsed.total_seconds()}\n")

    run_wrk_benchmark(shared_data)

    response = stop_workers()
    print(f"Time to stop workers: {response.elapsed.total_seconds()}\n")

    response = stop_workload()
    print(f"Time to stop workload: {response.elapsed.total_seconds()}\n")

    total_response_time = 0
    for i in range(NUMBER_DATABASES):
        response = remove_database(str(i))
        total_response_time = total_response_time + response.elapsed.total_seconds()
    print(f"Avg time to remove database: {total_response_time / NUMBER_DATABASES}\n")

    print_output(shared_data)
    formatted_reults = get_format_results(shared_data)
    path = create_folder()
    plot_bar_chart_throughput(formatted_reults, path, "throughput_comparison")
    write_to_csv(formatted_reults, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
