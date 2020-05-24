from .wrk_benchmark import run_wrk_parallel
from .wrk_benchmark_helper import (
    add_database,
    remove_database,
    start_workers,
    start_workload,
    stop_workers,
    stop_workload,
)

NUMBER_DATABASES = 3


def run_benchmark():
    for i in range(NUMBER_DATABASES):
        add_database(str(i))
    start_workload()
    start_workers()
    run_wrk_parallel()
    stop_workers()
    stop_workload()
    for i in range(NUMBER_DATABASES):
        remove_database(str(i))


if __name__ == "__main__":
    run_benchmark()  # type: ignore
