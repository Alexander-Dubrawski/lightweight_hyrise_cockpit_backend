from calendar import timegm
from datetime import datetime
from time import gmtime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure


def plot_matrix_sub_plot(row_labels, rows, col_labels):
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)


def plot_hdr_histogram(data, path, file_name):
    fig = figure(num=None, figsize=(30, 10), dpi=80, facecolor="w", edgecolor="k")
    for component, results in data.items():
        x_values = ["0%"]
        y_values = [0.0]
        for percentile, value in results["latency_distribution"].items():
            x_values.append(percentile)
            y_values.append(value)
        plt.plot(x_values, y_values, label=f"{component}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    plt.title("Latency by Percentile Distribution")
    plt.grid()
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_box_chart(data, path, file_name):
    fig = figure(num=None, figsize=(30, 20), dpi=80, facecolor="w", edgecolor="k")
    colors = ["cornflowerblue", "darkcyan", "indianred", "sandybrown"]
    position = 1
    x_labels = []
    for endpoint, results in data.items():
        c = colors[position - 1]
        data = results["latency_percentiles"]["percentiles"]
        plt.boxplot(
            data,
            boxprops=dict(facecolor=c),
            positions=[position],
            patch_artist=True,
            medianprops=dict(color="black"),
            flierprops=dict(marker="d", markerfacecolor="grey"),
        )
        position += 1
        x_labels.append(endpoint)
    plt.xticks([(i + 1) for i in range(position)], x_labels)
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Endpoints")
    plt.title("Latency by milliseconds")
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_box_chart_compare_parralel_sequential(
    data_sequential, data_parallel, path, file_name
):
    fig = figure(num=None, figsize=(30, 20), dpi=80, facecolor="w", edgecolor="k")
    colors = ["cornflowerblue", "darkcyan", "indianred", "sandybrown"]
    position = 0
    color_index = 0
    x_labels = []
    for endpoint, results in data_sequential.items():
        c = colors[color_index]
        sequential = results["latency_percentiles"]["percentiles"]
        parallel = data_parallel[endpoint]["latency_percentiles"]["percentiles"]
        plt.boxplot(
            [sequential, parallel],
            boxprops=dict(facecolor=c),
            positions=[position, position + 1],
            patch_artist=True,
            medianprops=dict(color="black"),
            flierprops=dict(marker="d", markerfacecolor="grey"),
        )
        position += 2
        x_labels.append(f"{endpoint}_sequential")
        x_labels.append(f"{endpoint}_parallel")
        color_index += 1
    plt.xticks([(i) for i in range(position)], x_labels)
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Endpoints")
    plt.title("Latency by milliseconds")
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_system_data(
    data,
    path,
    file_name,
    measurement_type,
    statistical_method,
    statistical_method_description,
    y_label,
):
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    formatted_system_values = []
    components = []
    for component, results in data.items():
        formatted_usage = [
            datetime.fromtimestamp(time_stamp) for time_stamp in results["time_stamp"]
        ]
        plt.plot(
            formatted_usage, results["usage"], label=f"{component} {measurement_type}",
        )
        formatted_system_values.append(
            f"{round(statistical_method(results['usage']), 2)}%"
        )
        components.append(component)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel(y_label)
    plt.xlabel("time")
    plt.title(measurement_type)
    row_labels = [statistical_method_description]
    rows = [formatted_system_values]
    plot_matrix_sub_plot(row_labels, rows, components)
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_comparison_parallel_sequential(
    sequential_data, parallel_data, path, metric_type, comparison_type, file_name, label
):
    endpoints = []
    parallel_values = []
    sequential_values = []
    for key, values in sequential_data.items():
        endpoints.append(key)
        sequential_values.append(values[metric_type][comparison_type])
        parallel_values.append(parallel_data[key][metric_type][comparison_type])

    ind = np.arange(len(endpoints))
    width = 0.20
    fig = figure(num=None, figsize=(40, 20), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(ind, parallel_values, width, label=f"parallel {comparison_type}")
    plt.bar(
        ind + width, sequential_values, width, label=f"sequenzial {comparison_type}"
    )
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel(label)
    plt.xlabel("Endpoints")
    plt.title(f"{comparison_type} {metric_type} per endpoint")
    plt.xticks(ind + width / 2, endpoints)
    if metric_type == "Latency":
        row_labels = [
            f"{comparison_type} in ms running parallel",
            f"{comparison_type} in ms running sequential",
        ]
    else:
        row_labels = [
            f"{comparison_type} in req/sec running parallel",
            f"{comparison_type} in req/sec running sequential",
        ]
    rows = [parallel_values, sequential_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_bar_chart(data, path, metric_type, file_name, label):
    endpoints = []
    avg_values = []
    stdev_values = []
    max_values = []
    for key, values in data.items():
        endpoints.append(key)
        avg_values.append(values[metric_type]["Avg"])
        stdev_values.append(values[metric_type]["Stdev"])
        max_values.append(values[metric_type]["Max"])

    ind = np.arange(len(endpoints))
    width = 0.20
    fig = figure(num=None, figsize=(40, 20), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(ind, stdev_values, width, label="Stdev")
    plt.bar(ind + width, avg_values, width, label="Avg")
    plt.bar(ind + (2 * width), max_values, width, label="Max")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel(label)
    plt.xlabel("Endpoints")
    plt.title(f"{metric_type} per endpoint")
    plt.xticks(ind + width, endpoints)
    if metric_type == "Latency":
        row_labels = ["Avg in ms", "Stdev in ms", "Max in ms"]
    else:
        row_labels = ["Avg in req/sec", "Stdev in req/sec", "Max in req/sec"]
    rows = [avg_values, stdev_values, max_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)
