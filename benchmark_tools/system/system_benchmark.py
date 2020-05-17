from calendar import timegm
from csv import writer
from datetime import datetime
from multiprocessing import Manager, Process
from os import mkdir
from subprocess import check_output
from time import gmtime, sleep, time

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT

DURATION = 30


def top_background_process(component, pid, shared_data):
    output = []
    start_time = time()
    end_time = start_time + DURATION
    current_time = start_time
    while current_time < end_time:
        current_time = time()
        results = (
            check_output(f"top -pid {pid} -l 1 | grep {pid}", shell=True)
            .decode("utf-8")
            .split()
        )
        results.insert(0, current_time)
        output.append(results)
        sleep(0.5)
    shared_data[component] = output


def create_wrapper_processes(pids, shared_data):
    return [
        Process(target=top_background_process, args=(component, pid, shared_data),)
        for component, pid in pids.items()
    ]


def get_pids():
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


def create_folder():
    ts = timegm(gmtime())
    path = f"measurements/system_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def write_to_csv(data, path):
    filednames = check_output("top -l 1 | grep PID", shell=True).decode("utf-8").split()
    filednames.insert(0, "time_stamp")
    for component, measurements in data.items():
        with open(f"{path}/system_data_{component}.csv", "w", newline="") as f:
            csv_writer = writer(f, delimiter="|")
            csv_writer.writerow(filednames)
            csv_writer.writerows(measurements)


def run_benchmark():
    manager = Manager()
    shared_data = manager.dict()
    pids = get_pids()
    path = create_folder()
    processes = create_wrapper_processes(pids, shared_data)
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()
    print
    write_to_csv(shared_data, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
