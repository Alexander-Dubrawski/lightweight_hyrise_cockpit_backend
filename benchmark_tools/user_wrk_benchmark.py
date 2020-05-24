from .wrk_benchmark import run_wrk_parallel, run_wrk_sequential
from .wrk_benchmark_helper import (
    add_database,
    create_folder,
    format_results,
    plot_results,
    print_results,
    remove_database,
    start_workers,
    start_workload,
    stop_workers,
    stop_workload,
    write_to_csv,
)

NUMBER_DATABASES = 3


def execute_benchmark(handler):
    for i in range(NUMBER_DATABASES):
        add_database(str(i))
    start_workload()
    start_workers()
    results = handler()
    stop_workers()
    stop_workload()
    for i in range(NUMBER_DATABASES):
        remove_database(str(i))
    return results


def run_benchmark():
    sequential_results = execute_benchmark(run_wrk_sequential)
    parallel_results = execute_benchmark(run_wrk_parallel)
    print_results(sequential_results, parallel_results)
    formatted_sequential_results = format_results(sequential_results)
    formatted_parallel_results = format_results(parallel_results)
    path = create_folder("user_wrk_benchmark")
    plot_results(path, formatted_sequential_results, formatted_parallel_results)
    write_to_csv(formatted_sequential_results, formatted_parallel_results, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
