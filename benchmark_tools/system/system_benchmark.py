from calendar import timegm
from csv import writer
from datetime import datetime
from multiprocessing import Manager, Process
from os import mkdir
from re import findall
from statistics import mean
from subprocess import check_output
from time import gmtime, sleep, time

from backend.settings import BACKEND_PORT, DB_MANAGER_PORT, GENERATOR_PORT
from benchmark_tools.graph_plotter import plot_system_data

DURATION = 30


def top_background_process(component, pid, shared_data):
    """Use top utility to determine system data for component."""
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


def create_folder():
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/system_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def get_memory_usage_in_m(usage):
    """Convert memory usage value to M."""
    m_metric_converter = {
        "B": lambda B: B / 1_000_000,
        "K": lambda K: K / 1_000,
        "M": lambda M: M,
        "G": lambda G: G * 1_000,
    }
    memory = findall(r"\d+", usage)[0]
    metric = findall(r"[A-Z]", usage)[0]
    return m_metric_converter[metric](int(memory))


def extract_memory_usage(data_set):
    """Extract memory usage."""
    measurements = {
        "usage": [],
        "time_stamp": [],
    }
    for data in data_set:
        measurements["usage"].append(get_memory_usage_in_m(data[8]))
        measurements["time_stamp"].append(data[0])
    return measurements


def extract_cpu_usgae(data_set):
    """Extract CPU usage."""
    measurements = {
        "usage": [],
        "time_stamp": [],
    }
    for data in data_set:
        measurements["usage"].append(float(data[3]))
        measurements["time_stamp"].append(data[0])
    return measurements


def plot_graph(data, path):
    """Plot graphs for every metric and component."""
    measurements = {
        "CPU": {
            "back_end": extract_cpu_usgae(data["back_end"]),
            "generator": extract_cpu_usgae(data["generator"]),
            "manager": extract_cpu_usgae(data["manager"]),
        },
        "MEMORY": {
            "back_end": extract_memory_usage(data["back_end"]),
            "generator": extract_memory_usage(data["generator"]),
            "manager": extract_memory_usage(data["manager"]),
        },
    }
    for measurement, components in measurements.items():
        plot_system_data(
            components,
            path,
            f"{measurement}_usage",
            f"{measurement} usage",
            mean,
            "AVG",
        )
        for component, results in components.items():
            plot_system_data(
                {component: results},
                path,
                f"{component}_{measurement}_usage",
                f"{measurement} usage",
                mean,
                "AVG",
            )


def write_to_csv(data, path):
    """Write benchmark results to CSV file."""
    filednames = check_output("top -l 1 | grep PID", shell=True).decode("utf-8").split()
    filednames.insert(0, "time_stamp")
    for component, measurements in data.items():
        with open(f"{path}/system_data_{component}.csv", "w", newline="") as f:
            csv_writer = writer(f, delimiter="|")
            csv_writer.writerow(filednames)
            csv_writer.writerows(measurements)


def run_benchmark():
    """
    Execute benchmark on all components parallel.

    Use a shared memory data-structured to get results from processes. Start one Process
    for every component and wait until they are done.
    """
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
    plot_graph(shared_data, path)
    write_to_csv(shared_data, path)


if __name__ == "__main__":
    run_benchmark()  # type: ignore
