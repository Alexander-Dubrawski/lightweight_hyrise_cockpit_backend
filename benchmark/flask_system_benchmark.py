# type: ignore
from csv import writer
from datetime import datetime
from multiprocessing import Process
from subprocess import CalledProcessError, check_output
from time import sleep

from backend.settings import BACKEND_PORT

NUMBER_PROCESSES = 80
NUMBER_TREADS = 1
SLEEP_DURATION = 1


def write_to_csv(data):
    """Write benchmark results to CSV file."""
    filednames = ["time_stamp", "pid", "%cpu", "%mem"]
    with open(
        f"measurements/system_backend_{NUMBER_PROCESSES}p_{NUMBER_TREADS}t.csv",
        "w",
        newline="",
    ) as f:
        csv_writer = writer(f, delimiter="|")
        csv_writer.writerow(filednames)
        csv_writer.writerows(data)


def fromat_avg_data(formatted_system_data):
    measurements = {
        "CPU": avg_usage(formatted_system_data, 2),
        "MEMORY": avg_usage(formatted_system_data, 3),
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
            measurements["usage"][-1] = round(
                measurements["usage"][-1] + float(data[index]), 3
            )
    return measurements


def format_data(row_data):
    formatted_lines = []
    for line in row_data:
        formatted_line = line
        formatted_line[0] = datetime.strptime(formatted_line[0], "%Y-%m-%d_%H:%M:%S")
        formatted_lines.append(formatted_line)
    return formatted_lines


def monitor_component(pids, duration):
    total_results = []
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
        total_results += [line.split() for line in result]
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
    return [backened_ppid] + get_child_pids(backened_ppid)


def run_wrk():
    out_put = check_output(
        "wrk -t80 -c80 -s ./benchmark_tools/report.lua -d11s http://127.0.0.1:8000/flask_metric",
        shell=True,
    ).decode("utf-8")
    print(out_put)


def run_ps():
    ppids = get_pids()
    p = Process(target=run_wrk)
    p.start()
    results = monitor_component(ppids, 10)
    p.join()
    return results


def monitor_system():

    results = run_ps()
    write_to_csv(results)
    formatted_data = format_data(results)
    formatted_avg = fromat_avg_data(formatted_data)
    print(formatted_avg)
    # plot_graph(formatted_data, path)


if __name__ == "__main__":
    monitor_system()
