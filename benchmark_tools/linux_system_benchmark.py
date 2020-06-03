from concurrent import futures
from subprocess import check_output
from time import sleep

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

DURATION = 40
SLEEP_DURATION = 0.5


def monitor_components(argument):
    component, pids = argument
    total_results = {component: []}
    runs = 0
    while runs < DURATION:
        results = (
            check_output(
                f"ps -p {','.join(pids)}  -o pid,%cpu,%mem | ts '%Y-%m-%d_%H:%M:%S'",
                shell=True,
            )
            .decode("utf-8")
            .splitlines()
        )
        results.pop(0)
        total_results[component] += [line.split() for line in results]
        sleep(SLEEP_DURATION)
        runs += SLEEP_DURATION
    return total_results


def get_child_pids(ppid):
    return check_output(f"pgrep -P {ppid}", shell=True).decode("utf-8").split()


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
        ("backened", [backened_ppid] + get_child_pids(backened_ppid)),
        ("generator", [generator_ppid] + get_child_pids(generator_ppid)),
        ("manager", [manager_ppid] + get_child_pids(manager_ppid)),
    ]


def run_benchmark():
    worker_thread = 3
    ppids = get_pids()
    with futures.ThreadPoolExecutor(worker_thread) as executor:
        _ = executor.map(monitor_components, ppids)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
