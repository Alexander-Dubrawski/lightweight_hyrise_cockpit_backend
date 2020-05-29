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

NUMBER_DATABASES = [1, 2, 10]


def execute_benchmark(handler, number_database):
    for i in range(number_database):
        add_database(str(i))
    start_workload()
    start_workers()
    results = handler()
    stop_workers()
    stop_workload()
    for i in range(number_database):
        remove_database(str(i))
    return results


def run_benchmark():
    for number_database in NUMBER_DATABASES:
        sequential_results = execute_benchmark(run_wrk_sequential, number_database)
        parallel_results = execute_benchmark(run_wrk_parallel, number_database)
        print_results(sequential_results, parallel_results)
        formatted_sequential_results = format_results(sequential_results)
        formatted_parallel_results = format_results(parallel_results)
        path = create_folder(f"user_wrk_benchmark_database_number_{number_database}")
        plot_results(path, formatted_sequential_results, formatted_parallel_results)
        write_to_csv(formatted_sequential_results, formatted_parallel_results, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
