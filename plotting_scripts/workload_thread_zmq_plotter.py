# type: ignore
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from .results_worker_thread_zmq import (
    latency_threads,
    latency_worker,
    thread_system,
    worker_system,
)


def plot_line_hdr_histogramm(data, metric):
    row_labels = []
    quantity = [1, 2, 4, 8, 16, 32, 40]
    percentile = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    rows = []
    for quan in quantity:
        row_labels.append(f"{quan} {metric}")
        x_values = [str(per) for per in percentile]
        y_values = data[quan]
        rows.append(data[quan])
        plt.plot(
            x_values, y_values, label=f"{quan} {metric}", linewidth=4.0,
        )
    return (rows, row_labels)


def plot_hdr_histogram(data, file_name, kind):
    fig = figure(num=None, figsize=(40, 40), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    rows, row_labels = plot_line_hdr_histogramm(data, kind)
    plt.legend()
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    plt.title("Latency by Percentile Distribution")
    plt.grid()
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.savefig(f"measurements/{file_name}.pdf")
    plt.close(fig)


def plot_hdr_historgram_for_system_data(data, duration, metric, kind):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [f"{s}sec" for s in range(duration)]
    rows = []
    row_labels = []
    for component, results in data.items():
        row_labels.append(f"{component} {kind}")
        row = []
        x_values = [i for i in range(duration)]
        y_values = []
        for value in results[metric]["usage"]:
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values, y_values, label=f"{component} {kind}t", linewidth=4.0,
        )
    plt.legend()
    plt.ylabel(f"{metric} usage (%)")
    plt.xlabel("time in sec")
    plt.title(f"{metric} usage of manager-end components")
    plt.grid()
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.savefig(f"measurements/manager_zmq_system_{metric}_{kind}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    plot_hdr_histogram(latency_worker, "zmq_hdr_processes", "Process")
    plot_hdr_histogram(latency_threads, "zmq_hdr_thread", "Thread")
    plot_hdr_historgram_for_system_data(worker_system, 10, "CPU", "Process")
    plot_hdr_historgram_for_system_data(thread_system, 10, "CPU", "Thread")
