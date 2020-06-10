# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

colors = {
    "running for 10s": "cornflowerblue",
    "running for 30s": "darkcyan",
    "running for 1m": "indianred",
    "running for 2m": "sandybrown",
    "running for 4m": "purple",
    "running for 8m": "aqua",
    "running for 16m": "magenta",
}


def plot_bar_chart(data, ax):
    x_labels = []
    width = 0.20
    x_values = []
    labels = data.keys()
    ind = np.arange(len(labels))
    for running_time, results in data.items():
        x_labels.append(running_time)
        x_values.append(results)
    ax.bar(ind, x_values, width, label="total number of requests")
    ax.legend()
    ax.set_ylabel("number of req")
    ax.set_title("Number of requests from wrk")
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )


def plot_hdr_histogram(data, ax, ax2):
    col_labels = list(data["running for 10s"].keys())
    row_labels = ["10s", "30s", "60s", "120s", "240s", "480s"]
    rows = []
    for running_time, results in data.items():
        row = []
        x_values = []
        y_values = []
        for percentile, value in results.items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        ax.plot(x_values, y_values, label=f"{running_time}")
        rows.append(row)
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("Percentile")
    ax.legend()
    ax.set_title("Latency by Percentile Distribution")
    ax.grid()
    ax2.axis("tight")
    ax2.axis("off")
    table = ax2.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="center",
        # bbox=[0, -0.29, 1, 0.17],
    )
    table.scale(1, 3)


def plot_graph(latency_data, throughput):
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(30, 15),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [30]
    hights = [10, 5]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax1 = fig.add_subplot(spec[0, 0])
    ax2 = fig.add_subplot(spec[1, 0])
    # fig, (ax1, ax2) = plt.subplots(
    #     2, 1, figsize=(30, 13), dpi=300, facecolor="w", edgecolor="k"
    # )
    # plot_bar_chart(throughput, ax1)
    plot_hdr_histogram(latency_data, ax1, ax2)
    # plt.tight_layout()
    fig.savefig("optimal_runtime_.pdf")
    plt.close(fig)


sequential_data = {
    "running for 10s": {
        "1%": 0.798,
        "25%": 0.815,
        "50%": 0.834,
        "75%": 0.891,
        "90%": 0.945,
        "99%": 1.586,
        "99.9%": 1.702,
        "99.99%": 2.172,
        "99.999%": 3.136,
    },
    "running for 30s": {
        "1%": 0.797,
        "25%": 0.814,
        "50%": 0.832,
        "75%": 0.874,
        "90%": 0.941,
        "99%": 1.574,
        "99.9%": 1.686,
        "99.99%": 1.938,
        "99.999%": 2.263,
    },
    "running for 1m": {
        "1%": 0.798,
        "25%": 0.813,
        "50%": 0.832,
        "75%": 0.872,
        "90%": 0.941,
        "99%": 1.571,
        "99.9%": 1.680,
        "99.99%": 1.832,
        "99.999%": 2.420,
    },
    "running for 2m": {
        "1%": 0.797,
        "25%": 0.814,
        "50%": 0.832,
        "75%": 0.876,
        "90%": 0.944,
        "99%": 1.566,
        "99.9%": 1.686,
        "99.99%": 13.384,
        "99.999%": 23.944,
    },
    "running for 4m": {
        "1%": 0.798,
        "25%": 0.814,
        "50%": 0.831,
        "75%": 0.866,
        "90%": 0.940,
        "99%": 1.556,
        "99.9%": 1.680,
        "99.99%": 6.135,
        "99.999%": 15.651,
    },
    "running for 8m": {
        "1%": 0.798,
        "25%": 0.814,
        "50%": 0.832,
        "75%": 0.871,
        "90%": 0.941,
        "99%": 1.556,
        "99.9%": 1.679,
        "99.99%": 1.845,
        "99.999%": 7.482,
    },
}


data_number_request_sequenzial = {
    "running for 10s": 10371,
    "running for 30s": 31256,
    "running for 1m": 62544,
    "running for 2m": 124992,
    "running for 4m": 250931,
    "running for 8m": 500965,
}


if __name__ == "__main__":
    plot_graph(sequential_data, data_number_request_sequenzial)
