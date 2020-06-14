# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from results_req_rep_zmq import req_rep_results

PERCENTILES = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]


def plot_hdr_histogram(results, ax, ax_table):
    col_labels = [f"{percentile}th" for percentile in PERCENTILES]
    rows = []
    row_labels = []
    for number, data in results.items():
        row_labels.append(f"clients: {number}")
        row = []
        y_values = []
        x_values = [str(percentile) for percentile in PERCENTILES]
        for value in data["latency distribution"]:
            y_values.append(value)
            row.append(value)
        rows.append(row)
        ax.plot(
            x_values, y_values, label=f"clients: {number}", linewidth=4.0,
        )
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
    ax_latency = fig.add_subplot(spec[0, 0])
    ax_latency_table = fig.add_subplot(spec[1, 0])
    plot_hdr_histogram(
        req_rep_results, ax_latency, ax_latency_table,
    )
    fig.savefig("req_rep_throughput_zmq.pdf")
    plt.close(fig)


if __name__ == "__main__":
    plot_graph()
