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
        x_values.append(mean(data[i : i + steps]))
        y_values.append(i)
    rounded_x_values = [round(value * 1000, 4) for value in x_values]
    return (rounded_x_values, y_values)


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


def plot_line_chart_avg_med(data, path, file_name, latency_type, interpolation_factor):
    avg_values = []
    med_values = []
    col_labels = []
    fig = figure(num=None, figsize=(30, 15), dpi=80, facecolor="w", edgecolor="k")
    for key, values in data.items():
        avg_values.append(f"{round(mean(values[latency_type]) * 1_000, 4)}ms")
        med_values.append(f"{round(median(values[latency_type]) * 1_000, 4)}ms")
        x_values, y_values = interpolate(values[latency_type], interpolation_factor)
        plt.plot(y_values, x_values, label=key)
        col_labels.append(key)

    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("time ms")
    plt.xlabel("runs")
    plt.title(latency_type)
    row_labels = ["AVG", "MED"]
    rows = [avg_values, med_values]
    plot_matrix_sub_plot(row_labels, rows, col_labels)
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
