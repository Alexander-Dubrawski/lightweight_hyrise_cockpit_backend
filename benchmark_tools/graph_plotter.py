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


def plot_line_chart(data, file_name, latency_type, interpolation_factor):
    avg_values = []
    med_values = []
    col_labels = []
    figure(num=None, figsize=(12, 6), dpi=80, facecolor="w", edgecolor="k")
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
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    ts = timegm(gmtime())
    plt.savefig(f"measurements/{file_name}_{ts}.png")


def plot_avg_med_bar_chart(data, file_name, latency_type):
    endpoints = []
    avg_values = []
    med_values = []
    row_avg_values = []
    row_med_values = []
    for key, values in data.items():
        avg_values.append(mean(values[latency_type]))
        med_values.append(median(values[latency_type]))
        row_avg_values.append(f"{round(mean(values[latency_type]) * 1_000, 4)}ms")
        row_med_values.append(f"{round(median(values[latency_type]) * 1_000, 4)}ms")
        endpoints.append(key)

    ind = np.arange(len(avg_values))
    width = 0.20
    figure(num=None, figsize=(20, 10), dpi=80, facecolor="w", edgecolor="k")
    plt.bar(ind, avg_values, width, label="AVG")
    plt.bar(ind + width, med_values, width, label="MED")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("time ms")
    plt.title("Latency per endpoint")
    plt.xticks(ind + width / 2, endpoints)

    row_labels = ["AVG", "MED"]
    rows = [row_avg_values, row_med_values]
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=endpoints,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)

    ts = timegm(gmtime())
    plt.savefig(f"measurements/{file_name}_{ts}.png")
