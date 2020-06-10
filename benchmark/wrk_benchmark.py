"""Tool for executing wrk benchmark."""
from multiprocessing import Manager, Process
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .system_benchmark import format_data, fromat_avg_data, monitor_system
from .system_benchmark import write_to_csv as system_write_to_csv
from .wrk_benchmark_helper import (
    add_database,
    create_folder,
    format_results,
    plot_charts,
    plot_system_data,
    print_results,
    print_user_results,
    remove_database,
    start_workers,
    start_workload,
    stop_workers,
    stop_workload,
)

NUMBER_CLIENTS = [1, 2, 4, 8, 16, 32, 80]
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 10
DURATION_IN_SECOUNDS_PARALLEL = 10
NUMBER_DATABASES = [1, 8, 80]
ENDPOINTS = ["manager_time_intense_metric", "manager_metric", "flask_metric"]


def execute_wrk_on_endpoint(url, number_clinets):
    """Background process to execute wrk."""
    return check_output(
        f"wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_SECOUNDS}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def wrk_background_process(url, endpoint, shared_data, number_clinets):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"wrk -t{number_clinets} -c{number_clinets} -s ./benchmark_tools/report.lua -d{DURATION_IN_SECOUNDS_PARALLEL}s --timeout 10s {url}",
        shell=True,
    ).decode("utf-8")


def create_wrk_processes(shared_data, number_client, enpoints):
    """Create one wrk process per endpoint."""
    return [
        Process(
            target=wrk_background_process,
            args=(f"{BACKEND_URL}/{end_point}", end_point, shared_data, number_client),
        )
        for end_point in enpoints
    ]


def run_wrk_sequential(enpoints):
    """Run wrk sequential on all endpoints."""
    sequential_results = {}
    for number_client in NUMBER_CLIENTS:
        sequential_results[number_client] = {}
        for endpoint in enpoints:
            sequential_results[number_client][endpoint] = execute_wrk_on_endpoint(
                f"{BACKEND_URL}/{endpoint}", number_client
            )
    return sequential_results


def run_wrk_parallel(enpoints):
    """Run wrk in parallel on all endpoints."""
    manager = Manager()
    parallel_results = {}
    for number_client in NUMBER_CLIENTS:
        shard_dict = manager.dict()
        processes = create_wrk_processes(shard_dict, number_client, enpoints)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
            process.terminate()
        parallel_results[number_client] = {}
        for key, value in shard_dict.items():
            parallel_results[number_client][key] = value
    return parallel_results


def execute_in_user_context(number_database):
    manager = Manager()
    parallel_results = {}
    shard_dict = manager.dict()
    for i in range(number_database):
        add_database(str(i))
    start_workload()
    start_workers()
    processes = create_wrk_processes(shard_dict, 1, ["manager_metric", "flask_metric"])
    for process in processes:
        process.start()
    monitor_system_data = monitor_system(DURATION_IN_SECOUNDS_PARALLEL)
    for process in processes:
        process.join()
        process.terminate()
    stop_workers()
    stop_workload()
    for i in range(number_database):
        remove_database(str(i))
    for key, value in shard_dict.items():
        parallel_results[key] = value
    return (parallel_results, monitor_system_data)


def run_user_benchmark(number_databases):
    results = {}
    system_data = {}
    for number_database in number_databases:
        parallel_results, monitor_system_data = execute_in_user_context(number_database)
        results[number_database] = parallel_results
        system_data[number_database] = monitor_system_data
    return (results, system_data)


def run_benchmark():
    """Run sequential and parallel wrk benchmark on endpoints."""
    print("Execute sequential")
    sequential_results = run_wrk_sequential(["manager_metric", "flask_metric"])
    # parallel_results = run_wrk_parallel(
    #     ["manager_time_intense_metric", "manager_metric"]
    # )
    print("Execute user")
    user_results, system_data = run_user_benchmark(NUMBER_DATABASES)
    print_results(sequential_results, None, NUMBER_CLIENTS)
    print_user_results(user_results)

    formatted_user_results = format_results(user_results)
    formatted_sequential_results = format_results(sequential_results)
    # formatted_parallel_results = format_results(parallel_results)
    formatted_system_data = format_data(system_data, NUMBER_DATABASES)
    measurements = fromat_avg_data(NUMBER_DATABASES, formatted_system_data)
    path = create_folder("wrk_benchmark")
    plot_system_data(measurements, path, DURATION_IN_SECOUNDS_PARALLEL, "CPU")
    plot_system_data(measurements, path, DURATION_IN_SECOUNDS_PARALLEL, "MEMORY")

    plot_charts(
        formatted_sequential_results,
        path,
        ("manager_metric", "flask_metric"),
        "theoretical_sequential",
        "client",
    )

    # plot_charts(
    #     formatted_parallel_results,
    #     path,
    #     ("manager_metric", "manager_time_intense_metric"),
    #     "theoretical_parallel",
    #     "client",
    # )

    plot_charts(
        formatted_user_results,
        path,
        ("manager_metric", "flask_metric"),
        "user",
        "database objects",
    )
    system_write_to_csv(formatted_system_data, path, NUMBER_DATABASES)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
