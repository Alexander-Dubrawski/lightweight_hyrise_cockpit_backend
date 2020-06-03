from concurrent import futures
from datetime import datetime
from subprocess import CalledProcessError, check_output
from time import sleep

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

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


def avg_usage(data_set, index):
    measurements = {
        "usage": [],
        "time_stamp": [],
    }
    last_ts = 0
    for data in data_set:
        current_ts = datetime.timestamp(data[0])
        if current_ts > last_ts:
            measurements["usage"].append(float(data[index]))
            measurements["time_stamp"].append(current_ts)
            last_ts = current_ts
        else:
            measurements["usage"][-1] = measurements["usage"][-1] + float(data[index])
    return measurements


def format_data(row_data):
    formatted_data = {}
    for component, results in row_data.items():
        formatted_lines = []
        for line in results:
            formatted_line = line
            formatted_line[0] = datetime.strptime(
                formatted_line[0], "%Y-%m-%d_%H:%M:%S"
            )
            formatted_lines.append(formatted_line)
        formatted_data[component] = formatted_lines
    return formatted_data


def run_benchmark():
    worker_thread = 3
    ppids = get_pids()
    with futures.ThreadPoolExecutor(worker_thread) as executor:
        res = executor.map(monitor_components, ppids)
    results = list(res)
    combined_res = {}
    for result in results:
        combined_res.update(result)
    formatted_res = format_data(combined_res)

    _ = {
        "CPU": {
            "back_end": avg_usage(formatted_res["back_end"], 2),
            "generator": avg_usage(formatted_res["generator"], 2),
            "manager": avg_usage(formatted_res["manager"], 2),
        },
        "MEMORY": {
            "back_end": avg_usage(formatted_res["back_end"], 3),
            "generator": avg_usage(formatted_res["generator"], 3),
            "manager": avg_usage(formatted_res["manager"], 3),
        },
    }


if __name__ == "__main__":
    run_benchmark()  # type: ignore
