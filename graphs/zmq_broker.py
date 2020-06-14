# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from zmq_broker_results import (
    single_latency,
    thread_result_latency,
    thread_result_throughput,
    worker_result_latency,
    worker_result_throughput,
)


def plot_bar(data_thread, data_worker, ax, ax_table):
    quantity = [1, 4, 16, 32, 64, 128]
    woker_values = []
    thread_values = []
    for quant in quantity:
        woker_values.append(data_worker[quant])
        thread_values.append(data_thread[quant])
    ind = np.arange(len(quantity))
    width = 0.20
    ax.bar(ind, woker_values, width, label="multi processing")
    ax.bar(ind + width, thread_values, width, label="multi threading")
    # barlist_processing[0].set_color("firebrick")
    # barlist_threading[0].set_color("firebrick")
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel("quantity threads/processes")
    ax.set_title("Throughput comparison ")
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(quantity)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[thread_values, woker_values],
        rowLabels=["multi threading", "multi processing"],
        cellLoc="center",
        colLabels=quantity,
        loc="center",
    )
    table.scale(1, 2)


def plot_line_hdr_histogramm(ax, data, metric):
    linestyles = {
        1: "-",
        4: "-",
        16: "-.",
        32: "--",
        64: ":",
        128: (0, (1, 10)),
    }
    x_values = [str(v) for v in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]]
    component_color = {
        "threads": "orange",
        "processes": "blue",
        "process & thread": "firebrick",
    }
    row_labels = []
    if metric == "process & thread":
        quantity = [1]
    else:
        quantity = [4, 16, 32, 64, 128]
    rows = []
    for quan in quantity:
        row_labels.append(f"{quan} {metric}")
        y_values = []
        row = []
        for value in data[quan]:
            y_values.append(value)
            row.append(value)
        rows.append(row)
        ax.plot(
            x_values,
            y_values,
            label=f"{quan} {metric}",
            linestyle=linestyles[quan],
            linewidth=4.0,
            color=component_color[metric],
        )
    return (rows, row_labels)


def plot_hdr(data_singel, data_thread, data_worker, ax, ax_table):
    col_labels = [
        f"{percentile}th"
        for percentile in [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
    ]
    single_rows, singel_labels = plot_line_hdr_histogramm(
        ax, data_singel, "process & thread"
    )
    thread_rows, thread_label = plot_line_hdr_histogramm(ax, data_thread, "threads")
    worker_rows, worker_labels = plot_line_hdr_histogramm(ax, data_worker, "processes")
    rows = single_rows + thread_rows + worker_rows
    row_labels = singel_labels + thread_label + worker_labels
    ax.legend()
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
        colLabels=col_labels,
        loc="center",
    )
    table.scale(1, 2)


def plot_graph():

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 13),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20]
    hights = [8, 5]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_io_latency = fig.add_subplot(spec[0, 0])
    ax_io_latency_table = fig.add_subplot(spec[1, 0])
    plot_hdr(
        single_latency,
        thread_result_latency,
        worker_result_latency,
        ax_io_latency,
        ax_io_latency_table,
    )
    fig.savefig("latency_thread_vs_worker_zmq.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 8),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10]
    hights = [5, 3]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_io_throughput = fig.add_subplot(spec[0, 0])
    ax_io_throughput_table = fig.add_subplot(spec[1, 0])
    plot_bar(
        thread_result_throughput,
        worker_result_throughput,
        ax_io_throughput,
        ax_io_throughput_table,
    )
    fig.savefig("throughput_thread_vs_worker_zmq.pdf")
    plt.close(fig)


if __name__ == "__main__":
    plot_graph()
