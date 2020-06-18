# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .broker_zmq_results import (
    detailed_thread_latency_1,
    detailed_worker_latency_1,
    detailed_worker_thread_latency_50,
    latency_threads_1,
    latency_threads_50,
    latency_threads_worker_1,
    latency_workers_1,
    latency_workers_50,
    throughput_threads_1,
    throughput_threads_50,
    throughput_threads_worker_1,
    throughput_threads_worker_50,
    throughput_workers_1,
    throughput_workers_50,
)


def plot_line_hdr_histogramm_detailed(data, title, p_type, ax, ax_table):
    percentiles = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99]
    percentiles = [f"{per}%" for per in percentiles]
    quantities = [2, 4, 8, 16, 32, 64, 128]
    component_color = {
        1: "orange",
        2: "blue",
        3: "darkgreen",
        4: "firebrick",
        8: "darkorchid",
        16: "grey",
        32: "darkkhaki",
        64: "lightpink",
        128: "red",
    }
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(quan)
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[str(quan)][percentile])
            row.append(data[str(quan)][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan}",
            linewidth=4.0,
            color=component_color[quan],
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.set_title(f"Latency by Percentile Distribution {title}")
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


def plot_line_hdr_histogramm_w_t_detailed(data, ax, ax_table):
    percentiles = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99]
    percentiles = [f"{per}%" for per in percentiles]
    quantities = [
        (2, 32),
        (3, 32),
        (4, 16),
        (3, 16),
        (2, 64),
    ]
    component_color = {
        (1, 1): "red",
        (2, 32): "blue",
        (3, 32): "darkgreen",
        (4, 16): "firebrick",
        (3, 16): "darkorchid",
        (2, 64): "orange",
    }
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(f"{quan[0]}p & {quan[1]}t")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[str(quan)][percentile])
            row.append(data[str(quan)][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{quan[0]}p & {quan[1]}t",
            linewidth=4.0,
            color=component_color[quan],
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


def plot_line_hdr_histogramm_w_t(data, ax, ax_table):
    percentiles = [
        "1%",
        "25%",
        "50%",
        "90%",
        "99%",
        "99.9%",
        "99.99%",
    ]
    quantities = [
        (2, 32),
        (3, 32),
        (4, 16),
        (3, 16),
        (2, 64),
    ]
    component_color = {
        (1, 1): "red",
        (2, 32): "blue",
        (3, 32): "darkgreen",
        (4, 16): "firebrick",
        (3, 16): "darkorchid",
        (2, 64): "orange",
    }
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(f"{quan[0]}p & {quan[1]}t")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[quan][percentile])
            row.append(data[quan][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{quan[0]}p & {quan[1]}t",
            linewidth=4.0,
            color=component_color[quan],
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


def plot_bar_w_t(data, ax, ax_table):
    quantities = [
        (2, 32),
        (3, 32),
        (4, 16),
        (3, 16),
        (2, 64),
    ]
    quantities_lables = [f"{quan[0]}p & {quan[1]}t" for quan in quantities]
    values = []
    for quan in quantities:
        values.append(data[quan])
    ind = np.arange(len(quantities))
    width = 0.60
    ax.bar(ind, values, width, label="req/sec")
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel("process & threads")
    ax.set_title("Throughput")
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities_lables)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[["%05.2f" % val for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=quantities_lables,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_bar_w_t_latency(data, ax, ax_table):
    quantities = [
        (2, 32),
        (3, 32),
        (4, 16),
        (3, 16),
        (2, 64),
    ]
    quantities_lables = [f"{quan[0]}p & {quan[1]}t" for quan in quantities]
    values = []
    for quan in quantities:
        values.append(data[quan]["50%"])
    ind = np.arange(len(quantities))
    width = 0.60
    ax.bar(ind, values, width, label="avg latency", color="orange")
    ax.legend()
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("process & threads")
    ax.set_title("Latency")
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities_lables)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[["%05.2f" % val for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=quantities_lables,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_line_hdr_histogramm(data, title, p_type, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%"]
    quantities = [1, 2, 4, 8, 16, 32, 64, 128]
    component_color = {
        1: "orange",
        2: "blue",
        3: "darkgreen",
        4: "firebrick",
        8: "darkorchid",
        16: "grey",
        32: "darkkhaki",
        64: "lightpink",
        128: "red",
    }
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(quan)
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[quan][percentile])
            row.append(data[quan][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan}",
            linewidth=4.0,
            color=component_color[quan],
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.set_title(f"Latency by Percentile Distribution {title}")
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


def plot_bar_latency(data, title, p_type, ax, ax_table):
    quantities = [1, 2, 4, 8, 16, 32, 64, 128]
    values = []
    for quan in quantities:
        values.append(data[quan]["50%"])
    ind = np.arange(len(quantities))
    width = 0.60
    if p_type == "threads":
        color = "orange"
    else:
        color = "blue"
    ax.bar(ind, values, width, label="avg latency", color=color)
    ax.legend()
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[["%06.2f" % val for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_bar(data, title, p_type, ax, ax_table):
    quantities = [1, 2, 4, 8, 16, 32, 64, 128]
    values = []
    for quan in quantities:
        values.append(data[quan])
    ind = np.arange(len(quantities))
    width = 0.60
    if p_type == "threads":
        color = "orange"
    else:
        color = "blue"
    ax.bar(ind, values, width, label="req/sec", color=color)
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[["%06.2f" % val for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def main():
    plt.rcParams.update({"font.size": 20})
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
    ax_latency_threads = fig.add_subplot(spec[0, 0])
    ax_latency_threads_table = fig.add_subplot(spec[1, 0])
    ax_latency_worker = fig.add_subplot(spec[0, 1])
    ax_latency_worker_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm(
        latency_threads_1,
        "threads (I/O 1ms)",
        "threads",
        ax_latency_threads,
        ax_latency_threads_table,
    )
    plot_line_hdr_histogramm(
        latency_workers_1,
        "processes (I/O 1ms)",
        "processes",
        ax_latency_worker,
        ax_latency_worker_table,
    )

    fig.savefig("broker_latency_1.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 20})
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
    ax_latency_threads = fig.add_subplot(spec[0, 0])
    ax_latency_threads_table = fig.add_subplot(spec[1, 0])
    ax_latency_worker = fig.add_subplot(spec[0, 1])
    ax_latency_worker_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm(
        latency_threads_50,
        "threads (I/O 50ms)",
        "threads",
        ax_latency_threads,
        ax_latency_threads_table,
    )
    plot_line_hdr_histogramm(
        latency_workers_50,
        "processes (I/O 50ms)",
        "processes",
        ax_latency_worker,
        ax_latency_worker_table,
    )

    fig.savefig("broker_latency_50.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 20})
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
    ax_latency_threads = fig.add_subplot(spec[0, 0])
    ax_latency_threads_table = fig.add_subplot(spec[1, 0])
    ax_latency_worker = fig.add_subplot(spec[0, 1])
    ax_latency_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar_latency(
        latency_threads_50,
        "Latency threads (I/O 50ms)",
        "threads",
        ax_latency_threads,
        ax_latency_threads_table,
    )
    plot_bar_latency(
        latency_workers_50,
        "Latency processes (I/O 50ms)",
        "processes",
        ax_latency_worker,
        ax_latency_worker_table,
    )

    fig.savefig("bar_broker_latency_50.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 6),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [6, 6]
    hights = [5, 1]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput_threads = fig.add_subplot(spec[0, 0])
    ax_throughput_threads_table = fig.add_subplot(spec[1, 0])
    ax_throughput_worker = fig.add_subplot(spec[0, 1])
    ax_throughput_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_threads_1,
        "Throughput threads (I/O 1ms)",
        "threads",
        ax_throughput_threads,
        ax_throughput_threads_table,
    )
    plot_bar(
        throughput_workers_1,
        "Throughput processes (I/O 1ms)",
        "processes",
        ax_throughput_worker,
        ax_throughput_worker_table,
    )

    fig.savefig("broker_throughput_1.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 6),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [6, 6]
    hights = [5, 1]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput_threads = fig.add_subplot(spec[0, 0])
    ax_throughput_threads_table = fig.add_subplot(spec[1, 0])
    ax_throughput_worker = fig.add_subplot(spec[0, 1])
    ax_throughput_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_threads_50,
        "Throughput threads (I/O 50ms)",
        "threads",
        ax_throughput_threads,
        ax_throughput_threads_table,
    )
    plot_bar(
        throughput_workers_50,
        "Throughput processes (I/O 50ms)",
        "processes",
        ax_throughput_worker,
        ax_throughput_worker_table,
    )

    fig.savefig("broker_throughput_50.pdf")
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
    ax_latency = fig.add_subplot(spec[0, 0])
    ax_latency_table = fig.add_subplot(spec[1, 0])
    # ax_throughput = fig.add_subplot(spec[0, 1])
    # ax_throughput_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm_w_t_detailed(
        detailed_worker_thread_latency_50, ax_latency, ax_latency_table
    )
    # plot_bar_w_t(throughput_threads_worker, ax_throughput, ax_throughput_table)

    fig.savefig("broker_combi_latency_50.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 6),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [12]
    hights = [5, 1]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput = fig.add_subplot(spec[0, 0])
    ax_throughput_table = fig.add_subplot(spec[1, 0])
    plot_bar_w_t(throughput_threads_worker_50, ax_throughput, ax_throughput_table)
    fig.savefig("broker_combi_throughput_50.pdf")
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
    ax_latency = fig.add_subplot(spec[0, 0])
    ax_latency_table = fig.add_subplot(spec[1, 0])
    # ax_throughput = fig.add_subplot(spec[0, 1])
    # ax_throughput_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm_w_t(latency_threads_worker_1, ax_latency, ax_latency_table)
    # plot_bar_w_t(throughput_threads_worker, ax_throughput, ax_throughput_table)

    fig.savefig("broker_combi_latency_1.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 6),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [12]
    hights = [5, 1]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput = fig.add_subplot(spec[0, 0])
    ax_throughput_table = fig.add_subplot(spec[1, 0])
    plot_bar_w_t(throughput_threads_worker_1, ax_throughput, ax_throughput_table)
    fig.savefig("broker_combi_throughput_1.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(28, 28),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [28]
    hights = [8, 6, 8, 6]
    spec = gridspec.GridSpec(
        ncols=1, nrows=4, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_latency_thread = fig.add_subplot(spec[0, 0])
    ax_latency_thread_table = fig.add_subplot(spec[1, 0])
    ax_latency_worker = fig.add_subplot(spec[2, 0])
    ax_latency_worker_table = fig.add_subplot(spec[3, 0])
    plot_line_hdr_histogramm_detailed(
        detailed_thread_latency_1,
        "threads (I/O 1ms)",
        "threads",
        ax_latency_thread,
        ax_latency_thread_table,
    )
    plot_line_hdr_histogramm_detailed(
        detailed_worker_latency_1,
        "processes (I/O 1ms)",
        "processes",
        ax_latency_worker,
        ax_latency_worker_table,
    )
    fig.savefig("detailed_latency_1.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
