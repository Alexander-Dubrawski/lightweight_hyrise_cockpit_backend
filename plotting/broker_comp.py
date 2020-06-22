# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .broker_comp_results import (
    latency_threads_balanced_1,
    latency_threads_balanced_50,
    latency_threads_not_balanced_1,
    latency_threads_not_balanced_50,
    latency_workers_balanced_1,
    latency_workers_balanced_50,
    latency_workers_balanced_slow,
    latency_workers_not_balanced_1,
    latency_workers_not_balanced_50,
    latency_workers_not_balanced_slow,
    throughput_threads_balanced_1,
    throughput_threads_balanced_50,
    throughput_threads_not_balanced_1,
    throughput_threads_not_balanced_50,
    throughput_workers_balanced_1,
    throughput_workers_balanced_50,
    throughput_workers_balanced_slow,
    throughput_workers_not_balanced_1,
    throughput_workers_not_balanced_50,
    throughput_workers_not_balanced_slow,
)


def plot_bar_latency(
    data_broker, data_balance, title, p_type, ax, ax_table, n_quan=None
):
    quantities = [1, 2, 4, 8, 16, 32, 64, 128]
    if n_quan:
        quantities = n_quan
    balance_values = []
    no_balance_value = []
    for quan in quantities:
        balance_values.append(data_balance[quan][0]["50%"])
        no_balance_value.append(data_broker[quan][0]["50%"])
    ind = np.arange(len(quantities))
    width = 0.20
    if p_type == "threads":
        no_balance_color = "orange"
        balance_color = "firebrick"
    else:
        no_balance_color = "blue"
        balance_color = "darkgreen"
    ax.bar(
        ind, balance_values, width, label="avg latency balanced", color=balance_color
    )
    ax.bar(
        ind + width,
        no_balance_value,
        width,
        label="avg latency not balanced",
        color=no_balance_color,
    )
    ax.legend()
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[
            ["%06.2f" % val for val in balance_values],
            ["%06.2f" % val for val in no_balance_value],
        ],
        rowLabels=["AVG balanced", "AVG not balanced"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_bar_throughput(
    data_broker, data_balance, title, p_type, ax, ax_table, n_quan=None
):
    quantities = [1, 2, 4, 8, 16, 32, 64, 128]
    if n_quan:
        quantities = n_quan
    balance_values = []
    no_balance_value = []
    for quan in quantities:
        balance_values.append(data_balance[quan][0])
        no_balance_value.append(data_broker[quan][0])
    ind = np.arange(len(quantities))
    width = 0.20
    if p_type == "threads":
        no_balance_color = "orange"
        balance_color = "firebrick"
    else:
        no_balance_color = "blue"
        balance_color = "darkgreen"
    ax.bar(ind, balance_values, width, label="req/sec balanced", color=balance_color)
    ax.bar(
        ind + width,
        no_balance_value,
        width,
        label="req/sec not balanced",
        color=no_balance_color,
    )
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[
            ["%06.2f" % val for val in balance_values],
            ["%06.2f" % val for val in no_balance_value],
        ],
        rowLabels=["req/sec balanced", "req/sec not balanced"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_line_hdr_histogramm(data_broker, data_balance, title, p_type, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%", "99.999%"]
    component_color = {
        16: "orange",
        32: "blue",
        64: "firebrick",
    }
    quantities = [16, 32, 64]
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(f"balanced {quan}")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data_balance[quan][0][percentile])
            row.append(data_balance[quan][0][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan}",
            linewidth=4.0,
            color=component_color[quan],
            linestyle="-",
        )
        row_labels.append(f"not balanced {quan}")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data_broker[quan][0][percentile])
            row.append(data_broker[quan][0][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan}",
            linewidth=4.0,
            color=component_color[quan],
            linestyle="--",
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.set_title("Latency by Percentile Distribution")
    ax.grid()
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=percentiles,
        loc="center",
    )
    table.scale(1, 3)
    table.set_fontsize(30)


def main():
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 10),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10, 10]
    hights = [7, 3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_latency(
        latency_threads_not_balanced_1,
        latency_threads_balanced_1,
        "threads (I/O 1ms)",
        "threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        latency_workers_not_balanced_1,
        latency_workers_balanced_1,
        "processes (I/O 1ms)",
        "processes",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("comp_latency_broker_1.pdf")
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
    widths = [10, 10]
    hights = [8, 2]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_throughput(
        throughput_threads_not_balanced_1,
        throughput_threads_balanced_1,
        "threads (I/O 1ms)",
        "threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_throughput(
        throughput_workers_not_balanced_1,
        throughput_workers_balanced_1,
        "processes (I/O 1ms)",
        "processes",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("comp_throughput_broker_1.pdf")
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
    widths = [10, 10]
    hights = [7, 3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_latency(
        latency_threads_not_balanced_50,
        latency_threads_balanced_50,
        "threads (I/O 50ms)",
        "threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        latency_workers_not_balanced_50,
        latency_workers_balanced_50,
        "processes (I/O 50ms)",
        "processes",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("comp_latency_broker_50.pdf")
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
    widths = [10, 10]
    hights = [8, 2]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_throughput(
        throughput_threads_not_balanced_50,
        throughput_threads_balanced_50,
        "threads (I/O 50ms)",
        "threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_throughput(
        throughput_workers_not_balanced_50,
        throughput_workers_balanced_50,
        "processes (I/O 50ms)",
        "processes",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("comp_throughput_broker_50.pdf")
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
    hights = [8, 2]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_down_left = fig.add_subplot(spec[1, 0])
    plot_bar_throughput(
        throughput_workers_not_balanced_slow,
        throughput_workers_balanced_slow,
        "Throughput",
        "processes",
        ax_top_left,
        ax_down_left,
        [16, 32, 64],
    )
    fig.savefig("comp_slow_worker_throughput_broker.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 12),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20]
    hights = [8, 4]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_down_left = fig.add_subplot(spec[1, 0])
    plot_line_hdr_histogramm(
        latency_workers_not_balanced_slow,
        latency_workers_balanced_slow,
        "Latency",
        "processes",
        ax_top_left,
        ax_down_left,
    )
    fig.savefig("comp_slow_worker_latency_broker.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
