from calendar import timegm
from statistics import mean, median
from time import gmtime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure


def interpolate(data, steps):
    x_values = []
    y_values = []
    for i in range(0, len(data), steps):
        y_values.append(mean(data[i : i + steps]))
        x_values.append(i)
    rounded_y_values = [round(value * 1000, 4) for value in y_values]
    return (x_values, rounded_y_values)


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
        plt.plot(
            results["time_stamp"],
            results["usage"],
            label=f"{component} {measurement_type}",
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
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)


def plot_line_chart(
    data,
    path,
    file_name,
    latency_type,
    interpolation_factor,
    statistical_method,
    statistical_method_description,
):
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    endpoints = []
    formatted_statistical_values = []
    for key, values in data.items():
        formatted_statistical_values.append(
            f"{round(statistical_method(values[latency_type]) * 1_000, 4)}ms"
        )
        x_values, y_values = interpolate(values[latency_type], interpolation_factor)
        plt.plot(x_values, y_values, label=key)
        endpoints.append(key)

    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("time ms")
    plt.xlabel("runs")
    plt.title(latency_type)
    row_labels = [statistical_method_description]
    rows = [formatted_statistical_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)


def plot_avg_med_bar_chart(data, path, file_name, latency_type):
    endpoints = []
    avg_values = []
    med_values = []
    row_avg_values = []
    row_med_values = []
    for key, values in data.items():
        avg_values.append(round(mean(values[latency_type]) * 1_000, 4))
        med_values.append(round(median(values[latency_type]) * 1_000, 4))
        row_avg_values.append(f"{round(mean(values[latency_type]) * 1_000, 4)}ms")
        row_med_values.append(f"{round(median(values[latency_type]) * 1_000, 4)}ms")
        endpoints.append(key)

    ind = np.arange(len(avg_values))
    width = 0.20
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(ind, avg_values, width, label="AVG")
    plt.bar(ind + width, med_values, width, label="MED")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("time ms")
    plt.title("Latency per endpoint")
    plt.xticks(ind + width / 2, endpoints)
    row_labels = ["AVG", "MED"]
    rows = [row_avg_values, row_med_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)


def plot_bar_chart(
    data,
    path,
    file_name,
    latency_type,
    statistical_method,
    statistical_method_description,
):
    endpoints = []
    statistical_values = []
    row_statistical_values = []
    for key, values in data.items():
        statistical_values.append(
            round(statistical_method(values[latency_type]) * 1_000, 4)
        )
        row_statistical_values.append(
            f"{round(statistical_method(values[latency_type]) * 1_000, 4)}ms"
        )
        endpoints.append(key)

    ind = np.arange(len(statistical_values))
    width = 0.20
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(ind, statistical_values, width, label=statistical_method_description)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("time ms")
    plt.title("Latency per endpoint")
    plt.xticks(ind + width / 2, endpoints)
    row_labels = [statistical_method_description]
    rows = [row_statistical_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)


def plot_bar_chart_throughput(data, path, file_name):
    endpoints = []
    throughput_values = []
    formatted_values = []
    for key, value in data.items():
        throughput_values.append(float(value))
        formatted_values.append(f"{value}/sec")
        endpoints.append(key)

    x_pos = [i for i, _ in enumerate(endpoints)]
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(x_pos, throughput_values, label="Requests/sec")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("Requests/sec")
    plt.title("Throughput per endpoint")
    plt.xticks(x_pos, endpoints)
    row_labels = ["Requests/sec"]
    rows = [formatted_values]
    plot_matrix_sub_plot(row_labels, rows, endpoints)

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)


def plot_stacked_bar_chart(data, path, file_name, statistical_method):
    endpoints = list(data.keys())
    server_process_times = np.array(
        [
            round(statistical_method(data[endpoint]["server_process_times"]) * 1_000, 4)
            for endpoint in endpoints
        ]
    )
    name_lookup_times = np.array(
        [
            round(statistical_method(data[endpoint]["name_lookup_times"]) * 1_000, 4)
            for endpoint in endpoints
        ]
    )
    connect_times = np.array(
        [
            round(statistical_method(data[endpoint]["connect_times"]) * 1_000, 4)
            for endpoint in endpoints
        ]
    )
    ind = np.arange(len(endpoints))
    width = 0.20
    fig = figure(num=None, figsize=(32, 16), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(
        ind,
        server_process_times,
        width,
        label="server_process_times",
        color="coral",
        bottom=name_lookup_times + connect_times,
    )
    plt.bar(
        ind,
        connect_times,
        width,
        label="connect_times",
        color="royalblue",
        bottom=name_lookup_times,
    )
    plt.bar(
        ind, name_lookup_times, width, label="name_lookup_times", color="lightslategrey"
    )
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.xticks(ind + width / 2, endpoints)
    plt.ylabel("time ms")
    plt.title("Latency distribution per endpoint")

    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.png")
    plt.close(fig)
