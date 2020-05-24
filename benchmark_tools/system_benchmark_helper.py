from calendar import timegm
from csv import writer
from datetime import datetime
from os import mkdir
from re import findall
from statistics import mean
from subprocess import check_output
from time import gmtime

from benchmark_tools.graph_plotter import plot_system_data


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
    last_ts = 0
    for data in data_set:
        current_ts = datetime.timestamp(data[0])
        if current_ts > last_ts:
            measurements["usage"].append(get_memory_usage_in_m(data[8]))
            measurements["time_stamp"].append(current_ts)
            last_ts = current_ts
        else:
            measurements["usage"][-1] = measurements["usage"][
                -1
            ] + get_memory_usage_in_m(data[8])
    return measurements


def extract_cpu_usgae(data_set):
    """Extract CPU usage."""
    measurements = {
        "usage": [],
        "time_stamp": [],
    }
    last_ts = 0
    for data in data_set:
        current_ts = datetime.timestamp(data[0])
        if current_ts > last_ts:
            measurements["usage"].append(float(data[3]))
            measurements["time_stamp"].append(current_ts)
            last_ts = current_ts
        else:
            measurements["usage"][-1] = measurements["usage"][-1] + float(data[3])
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
        if measurement == "CPU":
            y_label = "usage in %"
        else:
            y_label = "usage in M"
        plot_system_data(
            components,
            path,
            f"{measurement}_usage",
            f"{measurement} usage",
            mean,
            "AVG",
            y_label,
        )
        for component, results in components.items():
            plot_system_data(
                {component: results},
                path,
                f"{component}_{measurement}_usage",
                f"{measurement} usage",
                mean,
                "AVG",
                y_label,
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
