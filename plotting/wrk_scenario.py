# type: ignore
from datetime import timedelta
from statistics import median

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .wrk_scenario_results import cpu_usage, latency, throughput


def plot_cpu_usage(date, ax, component, number_dbs):
    component_color = {
        1: "orange",
        10: "blue",
        20: "darkgreen",
        40: "firebrick",
    }
    x_values = [str(timedelta(seconds=ts)) for ts in date[component]["time_stamp"]]
    y_values = date[component]["usage"]
    ax.plot(
        x_values,
        y_values,
        label=f"database obj {number_dbs}",
        linewidth=4.0,
        color=component_color[number_dbs],
    )
    ax.legend()
    ax.set_ylabel("CPU usage in %")
    ax.set_xlabel("time")
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 600))
    ax.set_title(f"CPU usage {component}")
    ax.grid()


def plot_hdr_histogramm_1_90(data, ax):
    percentiles = ["1%", "50%", "60%", "70%", "80%", "90%"]
    number_dbs = [1, 10, 20, 40]
    component_color = {
        1: "orange",
        10: "blue",
        20: "darkgreen",
        40: "firebrick",
    }
    row_labels = []
    rows = []
    for n_db in number_dbs:
        row_labels.append(n_db)
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[n_db][percentile])
            if percentile != "90%":
                row.append(data[n_db][percentile])
        rows.append(["%07.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"database obj {n_db}",
            linewidth=4.0,
            color=component_color[n_db],
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.set_title("Latency by Percentile Distribution")
    ax.grid()
    return (rows, row_labels, ["1%", "50%", "60%", "70%", "80%"])


def plot_hdr_histogramm_90_99(data, ax):
    percentiles = ["90%", "99%", "99.9%"]
    number_dbs = [1, 10, 20, 40]
    component_color = {
        1: "orange",
        10: "blue",
        20: "darkgreen",
        40: "firebrick",
    }
    row_labels = []
    rows = []
    for n_db in number_dbs:
        row_labels.append(n_db)
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[n_db][percentile])
            row.append(data[n_db][percentile])
        row.append(data[n_db]["99.99%"])
        rows.append(["%07.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"database obj {n_db}",
            linewidth=4.0,
            color=component_color[n_db],
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.set_title("Latency by Percentile Distribution")
    ax.grid()
    percentiles.append("99.99%")
    return (rows, row_labels, percentiles)


def plot_bar(data, ax, ax_table):
    number_dbs = [1, 10, 20, 40]
    values = []
    for number_db in number_dbs:
        values.append(data[number_db])
    ind = np.arange(len(number_dbs))
    width = 0.60
    ax.bar(ind, values, width, label="req/sec")
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel("Database obj")
    ax.set_title("Req/sec")
    ax.set_xticks(ind)
    ax.set_xticklabels(number_dbs)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[[str(val) for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=number_dbs,
        loc="center",
    )
    table.scale(1, 2)


def plot_bar_cpu(date, ax, ax_table, component):
    number_dbs = [1, 10, 20, 40]
    values = []
    for number_db in number_dbs:
        values.append(median(date[number_db][component]["usage"]))
    ind = np.arange(len(number_dbs))
    width = 0.60
    ax.bar(ind, values, width, label="avg CPU usage")
    ax.legend()
    ax.set_ylabel("CPU usage in %")
    ax.set_xlabel("Database obj")
    ax.set_title("AVG CPU usage in %")
    ax.set_xticks(ind)
    ax.set_xticklabels(number_dbs)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[[str(val) for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=number_dbs,
        loc="center",
    )
    table.scale(1, 2)


def main():
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(18, 10),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10, 8]
    hights = [7, 3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_io_latency_1_90 = fig.add_subplot(spec[0, 0])
    ax_io_latency_90_99 = fig.add_subplot(spec[0, 1])
    ax_io_latency_table = fig.add_subplot(spec[1, :])

    rows_1, row_labels_1, percentiles_1 = plot_hdr_histogramm_1_90(
        latency, ax_io_latency_1_90
    )
    rows_90, row_labels_90, percentiles_90 = plot_hdr_histogramm_90_99(
        latency, ax_io_latency_90_99
    )
    ax_io_latency_table.axis("tight")
    ax_io_latency_table.axis("off")
    table = ax_io_latency_table.table(
        cellText=[row_1 + row_90 for row_1, row_90 in zip(rows_1, rows_90)],
        rowLabels=row_labels_1,
        cellLoc="center",
        colLabels=percentiles_1 + percentiles_90,
        loc="center",
    )
    table.scale(1, 2)

    fig.savefig("user_scenario_latency.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 10),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20]
    hights = [7, 3]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput = fig.add_subplot(spec[0, 0])
    ax_througput_table = fig.add_subplot(spec[1, 0])
    plot_bar(throughput, ax_throughput, ax_througput_table)
    fig.savefig("user_scenario_throughput.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 10),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20]
    hights = [10]
    spec = gridspec.GridSpec(
        ncols=1, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_manager = fig.add_subplot(spec[0, 0])
    # ax_wsgi = fig.add_subplot(spec[0, 1])
    for n_db in [1, 10, 20, 40]:
        plot_cpu_usage(cpu_usage[n_db], ax_manager, "manager", n_db)
        # plot_cpu_usage(cpu_usage[n_db], ax_wsgi, "back_end", n_db)
    fig.savefig("user_scenario_cpu.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 10),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20]
    hights = [7, 3]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_usage = fig.add_subplot(spec[0, 0])
    ax_usage_table = fig.add_subplot(spec[1, 0])
    plot_bar_cpu(cpu_usage, ax_usage, ax_usage_table, "manager")
    fig.savefig("bar_cpu_usage.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
