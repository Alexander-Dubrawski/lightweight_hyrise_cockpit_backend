# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .wrk_user_results import (
    latency_flask,
    latency_manager,
    throughput_flask,
    throughput_manager,
)


def plot_line_hdr_histogramm(data, title, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%"]
    number_clients = [1, 2, 4, 8, 16, 32, 64]
    component_color = {
        1: "orange",
        2: "blue",
        3: "darkgreen",
        4: "firebrick",
        8: "darkorchid",
        16: "grey",
        32: "darkkhaki",
        64: "lightpink",
    }
    row_labels = []
    rows = []
    for n_client in number_clients:
        row_labels.append(n_client)
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data[n_client][percentile])
            row.append(data[n_client][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"clients {n_client}",
            linewidth=4.0,
            color=component_color[n_client],
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


def plot_bar(data, title, ax, ax_table):
    number_clients = [1, 2, 4, 8, 16, 32, 64]
    values = []
    for number_client in number_clients:
        values.append(data[number_client])
    ind = np.arange(len(number_clients))
    width = 0.60
    ax.bar(ind, values, width, label="req/sec")
    ax.legend()
    ax.set_ylabel("req/sec")
    ax.set_xlabel("clients")
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(number_clients)
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[["%04.1f" % val for val in values]],
        rowLabels=["AVG"],
        cellLoc="center",
        colLabels=number_clients,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def main():
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
    ax_io_flask_throughput = fig.add_subplot(spec[0, 0])
    ax_io_flask_throughput_table = fig.add_subplot(spec[1, 0])
    ax_io_manager_throughput = fig.add_subplot(spec[0, 1])
    ax_io_manager_throughput_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_flask,
        "Throughput flask_metric",
        ax_io_flask_throughput,
        ax_io_flask_throughput_table,
    )
    plot_bar(
        throughput_manager,
        "Throughput manager_metric",
        ax_io_manager_throughput,
        ax_io_manager_throughput_table,
    )
    fig.savefig("user_wrk_throughput.pdf")
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
    ax_io_flask_latency = fig.add_subplot(spec[0, 0])
    ax_io_flask_latency_table = fig.add_subplot(spec[1, 0])
    ax_io_manager_latency = fig.add_subplot(spec[0, 1])
    ax_io_manager_latency_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm(
        latency_flask, "flask_metric", ax_io_flask_latency, ax_io_flask_latency_table
    )
    plot_line_hdr_histogramm(
        latency_manager,
        "manager_metric",
        ax_io_manager_latency,
        ax_io_manager_latency_table,
    )
    fig.savefig("user_wrk_latency.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
