# type: ignore
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure

from .results_worker_thread_flask import (
    combination_system_usage,
    latency_thread_no_i_o,
    latency_thread_with_i_o,
    latency_worker_no_i_o,
    latency_worker_thread_compination,
    latency_worker_with_i_o,
    throughput_thread_no_i_o,
    throughput_thread_with_i_o,
    throughput_worker_no_i_o,
    throughput_worker_thread_compination,
    throughput_worker_with_i_o,
)


def plot_hdr_historgram_for_system_data(data, duration, metric):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [f"{s}sec" for s in range(duration)]
    rows = []
    row_labels = []
    for component, results in data.items():
        row_labels.append(f"{component[0]}p & {component[1]}t")
        row = []
        x_values = [i for i in range(duration)]
        y_values = []
        for value in results[metric]["usage"]:
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values,
            y_values,
            label=f"{component[0]}p & {component[1]}t",
            linewidth=4.0,
        )
    plt.legend()
    plt.ylabel(f"{metric} usage (%)")
    plt.xlabel("time in sec")
    plt.title(f"{metric} usage of back-end components")
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
    plt.savefig(f"measurements/system_{metric}.pdf")
    plt.close(fig)


def plot_line_hdr_histogramm(data, metric):
    linestyles = {
        4: "-",
        16: "-.",
        32: "--",
        80: ":",
        160: (0, (3, 1, 1, 1, 1, 1)),
    }
    component_color = {
        "threads": "orange",
        "processes": "blue",
    }
    row_labels = []
    quantity = [4, 16, 32, 80, 160]
    rows = []
    for quan in quantity:
        row_labels.append(f"{quan} {metric}")
        x_values = []
        y_values = []
        row = []
        for percentile, value in data[quan].items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values,
            y_values,
            label=f"{quan} {metric}",
            linestyle=linestyles[quan],
            linewidth=4.0,
            color=component_color[metric],
        )
    return (rows, row_labels)


def plot_hdr_histogram(data_worker, data_thread, file_name, io_duration):
    fig = figure(num=None, figsize=(40, 40), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    thread_rows, thread_label = plot_line_hdr_histogramm(data_thread, "threads")
    worker_rows, worker_labels = plot_line_hdr_histogramm(data_worker, "processes")
    rows = thread_rows + worker_rows
    row_labels = thread_label + worker_labels
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


def plot_bar_chart(data_worker, data_thread, file_name):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    quantity = [4, 16, 32, 80, 160]
    woker_values = []
    thread_values = []
    for quant in quantity:
        woker_values.append(data_worker[quant]["Avg"])
        thread_values.append(data_thread[quant]["Avg"])
    ind = np.arange(len(quantity))
    width = 0.20
    plt.bar(ind, woker_values, width, label="multi threading")
    plt.bar(ind + width, thread_values, width, label="multi threading")
    plt.legend()
    plt.ylabel("req/sec")
    plt.xlabel("quantity threads/processes")
    plt.title("Throughput comparison")
    plt.xticks(ind + width / 2, quantity)
    plt.table(
        cellText=[thread_values, woker_values],
        rowLabels=["multi threading", "multi processing"],
        cellLoc="center",
        colLabels=quantity,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.savefig(f"measurements/{file_name}.pdf")
    plt.close(fig)


def plot_hdr_histogram_combination(data, file_name):
    fig = figure(num=None, figsize=(40, 40), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    row_labels = []
    quantity = [(80, 1), (4, 20), (3, 27), (2, 40), (8, 10)]
    rows = []
    for quan in quantity:
        row_labels.append(f"{quan[0]}p & {quan[1]}t")
        x_values = []
        y_values = []
        row = []
        for percentile, value in data[quan].items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values, y_values, label=f"{quan[0]}p & {quan[1]}t", linewidth=4.0,
        )
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


def plot_bar_chart_combination(data, file_name):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    quantity = [(80, 1), (4, 20), (3, 27), (2, 40), (8, 10)]
    colLabels = [f"{quan[0]}p & {quan[1]}t" for quan in quantity]
    values = []
    for quant in quantity:
        values.append(data[quant]["Avg"])
    ind = np.arange(len(quantity))
    width = 0.20
    plt.bar(ind, values, width, label="threads per processes")
    plt.legend()
    plt.ylabel("req/sec")
    plt.xlabel("quantity threads per processes")
    plt.title("Throughput comparison")
    plt.xticks(ind, colLabels)
    plt.table(
        cellText=[values],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=colLabels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.savefig(f"measurements/{file_name}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    plot_bar_chart(throughput_worker_no_i_o, throughput_thread_no_i_o, "bar_no_io")
    plot_bar_chart(
        throughput_worker_with_i_o, throughput_thread_with_i_o, "bar_with_io"
    )
    plot_hdr_histogram(latency_worker_with_i_o, latency_thread_with_i_o, "hdr_with_io")
    plot_hdr_histogram(latency_worker_no_i_o, latency_thread_no_i_o, "hdr_no_io")
    plot_bar_chart_combination(throughput_worker_thread_compination, "bar_combination")
    plot_hdr_histogram_combination(latency_worker_thread_compination, "hdr_combination")
    plot_hdr_historgram_for_system_data(combination_system_usage, 10, "CPU")
