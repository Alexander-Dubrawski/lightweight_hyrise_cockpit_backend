"""Tool for executing wrk benchmark."""
from calendar import timegm
from datetime import datetime
from json import dumps
from multiprocessing import Manager, Process
from os import mkdir
from subprocess import check_output
from time import gmtime

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .system_benchmark import format_data, fromat_avg_data, monitor_system, write_to_csv
from .wrk_benchmark_helper import (
    add_database,
    format_results,
    plot_system_data,
    print_user_results,
    remove_database,
    start_workers,
    start_workload,
    stop_workers,
    stop_workload,
)

NUMBER_CLIENTS = 1
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_MINUTES = 60
NUMBER_DATABASES = [1, 10, 20, 40]
ENDPOINT = "manager_metric"


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def wrk_background_process(url, endpoint, shared_data):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"wrk -t{NUMBER_CLIENTS} -c{NUMBER_CLIENTS} -s ./benchmark_tools/report.lua -d{DURATION_IN_MINUTES}m --timeout 20s {url}",
        shell=True,
    ).decode("utf-8")


def create_wrk_processes(shared_data, number_client, enpoints):
    """Create one wrk process per endpoint."""
    Process(
        target=wrk_background_process,
        args=(f"{BACKEND_URL}/{ENDPOINT}", ENDPOINT, shared_data),
    )


def execute_in_user_context(number_database):
    manager = Manager()
    results = {}
    shard_dict = manager.dict()
    for i in range(number_database):
        add_database(str(i))
    start_workload()
    start_workers()
    processes = create_wrk_processes(shard_dict, 8, ["manager_metric", "flask_metric"])
    for process in processes:
        process.start()
    monitor_system_data = monitor_system(DURATION_IN_MINUTES * 60)
    for process in processes:
        process.join()
        process.terminate()
    stop_workers()
    stop_workload()
    for i in range(number_database):
        remove_database(str(i))
    for key, value in shard_dict.items():
        results[key] = value
    return (results, monitor_system_data)


def run_user_benchmark(number_databases, path):
    results = {}
    system_data = {}
    for number_database in number_databases:
        parallel_results, monitor_system_data = execute_in_user_context(number_database)
        results[number_database] = parallel_results
        system_data[number_database] = monitor_system_data
        write_to_csv(system_data, path, [number_database])
        with open(f"{path}/{number_database}_results.txt", "+w") as file:
            file.write(dumps(parallel_results))
        with open(
            f"{path}/{number_database}_formatted_system_results.txt", "+w"
        ) as file:
            file.write(dumps(format_data(system_data, [number_database])))
    return (results, system_data)


def run_benchmark():
    path = create_folder("user_wrk_benchmark")
    user_results, system_data = run_user_benchmark(NUMBER_DATABASES, path)
    print_user_results(user_results)
    formatted_user_results = format_results(user_results)
    formatted_system_data = format_data(system_data, NUMBER_DATABASES)
    measurements = fromat_avg_data(NUMBER_DATABASES, formatted_system_data)
    with open(f"{path}/measurements_system.txt", "+w") as file:
        file.write(dumps(measurements))
    with open(f"{path}/formatted_user_results.txt", "+w") as file:
        file.write(dumps(formatted_user_results))
    write_to_csv(formatted_system_data, path, NUMBER_DATABASES)
    plot_system_data(measurements, path, DURATION_IN_MINUTES * 60, "CPU")
    plot_system_data(measurements, path, DURATION_IN_MINUTES * 60, "MEMORY")
