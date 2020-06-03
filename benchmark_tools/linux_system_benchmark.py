from concurrent import futures
from subprocess import CalledProcessError, check_output
from time import sleep

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

from .linux_system_benchmark_helper import (
    create_folder,
    format_data,
    plot_graph,
    write_to_csv,
)

DURATION = 2
SLEEP_DURATION = 1


def monitor_components(argument):
    component, pids = argument
    total_results = {component: []}
    row_results = []
    run = 0
    while run < DURATION:
        row_results.append(
            check_output(
                f"ps -p {','.join(pids)}  -o pid,%cpu,%mem | ts '%Y-%m-%d_%H:%M:%S'",
                shell=True,
            )
        )
        sleep(1)
        run += SLEEP_DURATION

    for row_result in row_results:
        result = row_result.decode("utf-8").splitlines()
        result.pop(0)
        total_results[component] += [line.split() for line in result]
    return total_results


def get_child_pids(ppid):
    try:
        return check_output(f"pgrep -P {ppid}", shell=True).decode("utf-8").split()
    except CalledProcessError:
        return []


def get_pids():
    backened_ppid = (
        check_output(f"lsof -n -i :{BACKEND_PORT} | grep LISTEN", shell=True)
        .decode("utf-8")
        .split()[1]
    )
    generator_ppid = (
        check_output(f"lsof -n -i :{GENERATOR_PORT} | grep LISTEN", shell=True)
        .decode("utf-8")
        .split()[1]
    )
    manager_ppid = (
        check_output(f"lsof -n -i :{DB_MANAGER_PORT} | grep LISTEN", shell=True)
        .decode("utf-8")
        .split()[1]
    )
    return [
        ("back_end", [backened_ppid] + get_child_pids(backened_ppid)),
        ("generator", [generator_ppid] + get_child_pids(generator_ppid)),
        ("manager", [manager_ppid] + get_child_pids(manager_ppid)),
    ]


def run_ps():
    worker_thread = 3
    ppids = get_pids()
    with futures.ThreadPoolExecutor(worker_thread) as executor:
        res = executor.map(monitor_components, ppids)
    results = list(res)
    combined_res = {}
    for result in results:
        combined_res.update(result)
    return combined_res


def run_benchmark():

    results = run_ps()
    path = create_folder()
    write_to_csv(results, path)
    formatted_data = format_data(results)
    plot_graph(formatted_data, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
