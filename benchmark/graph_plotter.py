from calendar import timegm
from time import gmtime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure


def plot_sub_bar_chart(ax, data, endpoint, metric_type, label, x_label):
    clients = []
    avg_values = []
    stdev_values = []
    max_values = []
    for key, values in data.items():
        clients.append(key)
        avg_values.append(values[endpoint][metric_type]["Avg"])
        stdev_values.append(values[endpoint][metric_type]["Stdev"])
        max_values.append(values[endpoint][metric_type]["Max"])

    ind = np.arange(len(clients))
    width = 0.20
    ax.bar(ind, stdev_values, width, label="Stdev")
    ax.bar(ind + width, avg_values, width, label="Avg")
    ax.bar(ind + (2 * width), max_values, width, label="Max")
    ax.legend()
    ax.set_ylabel(label)
    ax.set_xlabel(x_label)
    ax.set_title(f"{metric_type} for {endpoint}")
    ax.set_xticks(ind + width, minor=False)
    ax.set_xticklabels(clients, fontdict=None, minor=False)
    ax.table(
        cellText=[avg_values, stdev_values, max_values],
        rowLabels=["Avg", "Stdev", "Max"],
        cellLoc="center",
        colLabels=clients,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )


def plot_bar_chart_for_endpoint(
    data, path, metric_type, file_name, label, enpoints, x_label
):
    endpoint_one, endpoint_two = enpoints
    plt.rcParams.update({"font.size": 22})
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(30, 30), dpi=300, facecolor="w", edgecolor="k"
    )
    plot_sub_bar_chart(ax1, data, endpoint_one, metric_type, label, x_label)
    plot_sub_bar_chart(ax2, data, endpoint_two, metric_type, label, x_label)
    plt.tight_layout()
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_hdr_historgram_for_system_data(results, path, duration, metric):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [f"{s}sec" for s in range(duration)]
    linestyles = {1: "-", 10: ":", 20: "-.", 40: "--", 80: "-."}
    component_color = {
        "back_end": "orange",
        "generator": "blue",
        "manager": "purple",
    }
    rows = []
    row_labels = []
    for number, data in results.items():
        for component, results in data[metric].items():
            row_labels.append(f"{component} & {number} database object")
            row = []
            x_values = [i for i in range(duration)]
            y_values = []
            for value in results["usage"]:
                y_values.append(value)
                row.append(value)
            rows.append(row)
            plt.plot(
                x_values,
                y_values,
                label=f"{component} & {number} database object",
                linestyle=linestyles[number],
                linewidth=4.0,
                color=component_color[component],
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
    ts = timegm(gmtime())
    plt.savefig(f"{path}/system_{metric}_{ts}.pdf")
    plt.close(fig)


def plot_hdr_histogram_for_single_endpoint(
    results, path, file_name, label_type, component, title_name=None
):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    rows = []
    row_labels = []
    for number, data in results.items():
        row_labels.append(f"{component} & {number} {label_type}")
        row = []
        x_values = []
        y_values = []
        for percentile, value in data[component]["latency_distribution"].items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values,
            y_values,
            label=f"{component} & {number} {label_type}",
            linewidth=4.0,
        )
    plt.legend()
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    if title_name:
        plt.title(title_name)
    else:
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
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)


def plot_hdr_histogram_for_endpoint(
    results, path, file_name, label_type, title_name=None
):
    fig = figure(num=None, figsize=(40, 40), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    linestyles = {
        1: "-",
        2: ":",
        4: (0, (5, 1)),
        8: (0, (5, 5)),
        10: (0, (5, 10)),
        16: (0, (5, 10)),
        32: (0, (3, 1, 1, 1, 1, 1)),
        40: (0, (3, 1, 1, 1, 1, 1)),
        64: (0, (3, 10, 1, 10, 1, 10)),
    }
    component_color = {
        "manager_metric": "orange",
        "flask_metric": "blue",
        "manager_time_intense_metric": "purple",
    }
    rows = []
    row_labels = []
    for number, data in results.items():
        for component, results in data.items():
            row_labels.append(f"{component} & {number} {label_type}")
            row = []
            x_values = []
            y_values = []
            for percentile, value in results["latency_distribution"].items():
                x_values.append(percentile)
                y_values.append(value)
                row.append(value)
            rows.append(row)
            plt.plot(
                x_values,
                y_values,
                label=f"{component} & {number} {label_type}",
                linestyle=linestyles[number],
                linewidth=4.0,
                color=component_color[component],
            )
    plt.legend()
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    if title_name:
        plt.title(title_name)
    else:
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
    ts = timegm(gmtime())
    plt.savefig(f"{path}/{file_name}_{ts}.pdf")
    plt.close(fig)
