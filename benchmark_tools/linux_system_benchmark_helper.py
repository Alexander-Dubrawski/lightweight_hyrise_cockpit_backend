from calendar import timegm
from csv import writer
from datetime import datetime
from os import mkdir
from statistics import mean
from time import gmtime

from benchmark_tools.graph_plotter import plot_system_data


def create_folder():
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/system_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


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


def plot_graph(data, path):
    """Plot graphs for every metric and component."""
    measurements = {
        "CPU": {
            "back_end": avg_usage(data["back_end"], 2),
            "generator": avg_usage(data["generator"], 2),
            "manager": avg_usage(data["manager"], 2),
        },
        "MEMORY": {
            "back_end": avg_usage(data["back_end"], 3),
            "generator": avg_usage(data["generator"], 3),
            "manager": avg_usage(data["manager"], 3),
        },
    }
    for measurement, components in measurements.items():
        if measurement == "CPU":
            y_label = "usage in %"
        else:
            y_label = "usage in %"
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
    filednames = ["time_stamp", "pid", "%cpu", "%mem"]
    filednames.insert(0, "time_stamp")
    for component, measurements in data.items():
        with open(f"{path}/system_data_{component}.csv", "w", newline="") as f:
            csv_writer = writer(f, delimiter="|")
            csv_writer.writerow(filednames)
            csv_writer.writerows(measurements)
