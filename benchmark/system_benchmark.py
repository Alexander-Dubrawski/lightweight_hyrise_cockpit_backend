from concurrent import futures
from csv import writer
from datetime import datetime
from subprocess import CalledProcessError, check_output
from time import sleep

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

SLEEP_DURATION = 1


def write_to_csv(data, path, number_databases):
    """Write benchmark results to CSV file."""
    filednames = ["time_stamp", "pid", "%cpu", "%mem"]
    for number_database in number_databases:
        for component, measurements in data[number_database].items():
            with open(
                f"{path}/system_data_db{number_database}_{component}.csv",
                "w",
                newline="",
            ) as f:
                csv_writer = writer(f, delimiter="|")
                csv_writer.writerow(filednames)
                csv_writer.writerows(measurements)


def fromat_avg_data(number_databases, formatted_system_data):
    measurements = {}
    for number_database in number_databases:
        measurements[number_database] = {
            "CPU": {
                "back_end": avg_usage(
                    formatted_system_data[number_database]["back_end"], 2
                ),
                "generator": avg_usage(
                    formatted_system_data[number_database]["generator"], 2
                ),
                "manager": avg_usage(
                    formatted_system_data[number_database]["manager"], 2
                ),
            },
            "MEMORY": {
                "back_end": avg_usage(
                    formatted_system_data[number_database]["back_end"], 3
                ),
                "generator": avg_usage(
                    formatted_system_data[number_database]["generator"], 3
                ),
                "manager": avg_usage(
                    formatted_system_data[number_database]["manager"], 3
                ),
            },
        }
    return measurements


def avg_usage(data_set, index):
    measurements = {
        "usage": [],
        "time_stamp": [],
    }
    last_ts = 0
    currend_secound = 0
    for data in data_set:
        current_ts = datetime.timestamp(data[0])
        if current_ts > last_ts:
            measurements["usage"].append(float(data[index]))
            measurements["time_stamp"].append(currend_secound)
            last_ts = current_ts
            currend_secound += 1
        else:
            measurements["usage"][-1] = measurements["usage"][-1] + float(data[index])
    return measurements


def format_data(row_data, number_databases):
    formatted_data = {}
    for number_database in number_databases:
        formatted_data[number_database] = {}
        for component, results in row_data[number_database].items():
            formatted_lines = []
            for line in results:
                formatted_line = line
                formatted_line[0] = datetime.strptime(
                    formatted_line[0], "%Y-%m-%d_%H:%M:%S"
                )
                formatted_lines.append(formatted_line)
            formatted_data[number_database][component] = formatted_lines
    return formatted_data


def monitor_components(argument):
    component, pids, duration = argument
    total_results = {component: []}
    row_results = []
    run = 0
    while run < duration:
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


def get_pids(duration):
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
        ("back_end", [backened_ppid] + get_child_pids(backened_ppid), duration),
        ("generator", [generator_ppid] + get_child_pids(generator_ppid), duration),
        ("manager", [manager_ppid] + get_child_pids(manager_ppid), duration),
    ]


def run_ps(duration):
    worker_thread = 3
    ppids = get_pids(duration)
    with futures.ThreadPoolExecutor(worker_thread) as executor:
        res = executor.map(monitor_components, ppids)
    results = list(res)
    combined_res = {}
    for result in results:
        combined_res.update(result)
    return combined_res


def monitor_system(duration):

    return run_ps(duration)
    # path = create_folder()
    # write_to_csv(results, path)
    # formatted_data = format_data(results)
    # plot_graph(formatted_data, path)
