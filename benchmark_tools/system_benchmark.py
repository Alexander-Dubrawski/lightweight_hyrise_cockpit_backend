from multiprocessing import Manager, Process
from subprocess import check_output

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

from .system_benchmark_helper import (
    create_folder,
    format_data,
    plot_graph,
    write_to_csv,
)
from .user_wrk_benchmark import execute_benchmark
from .wrk_benchmark import run_wrk_parallel

DURATION = 62


def top_background_process(component, pid, shared_data):
    """Use top utility to determine system data for component."""
    output = check_output(
        f"top -l {DURATION} | ts '%Y-%m-%d_%H:%M:%S' | grep {pid}", shell=True
    ).decode("utf-8")
    output = output.splitlines()
    shared_data[component] = [line.split() for line in output]


def create_wrapper_processes(pids, shared_data):
    return [
        Process(target=top_background_process, args=(component, pid, shared_data),)
        for component, pid in pids.items()
    ]


def get_pids():
    """
    Get PID from every component.

    Use lsof to determine PID from Components.

    Return:
        Dictionary:
            back_end: PID of back-end component
            generator: PID of generator component
            manager: PID of manager component
    """
    return {
        "back_end": check_output(
            f"lsof -n -i :{BACKEND_PORT} | grep LISTEN", shell=True
        )
        .decode("utf-8")
        .split()[1],
        "generator": check_output(
            f"lsof -n -i :{GENERATOR_PORT} | grep LISTEN", shell=True
        )
        .decode("utf-8")
        .split()[1],
        "manager": check_output(
            f"lsof -n -i :{DB_MANAGER_PORT} | grep LISTEN", shell=True
        )
        .decode("utf-8")
        .split()[1],
    }


def run_top():
    manager = Manager()
    shared_data = manager.dict()
    pids = get_pids()
    processes = create_wrapper_processes(pids, shared_data)
    for process in processes:
        process.start()

    execute_benchmark(run_wrk_parallel)

    for process in processes:
        process.join()
        process.terminate()
    results = {}
    for key, value in shared_data.items():
        results[key] = value
    return results


def run_benchmark():
    """
    Execute benchmark on all components parallel.

    Use a shared memory data-structured to get results from processes. Start one Process
    for every component and wait until they are done.
    """
    results = run_top()
    path = create_folder()
    write_to_csv(results, path)
    formatted_data = format_data(results)
    plot_graph(formatted_data, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
