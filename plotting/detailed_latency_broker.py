# type: ignore
# flake8: noqa
from json import loads
from statistics import mean, median, pstdev

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


def get_latency(number, io_length, kind):
    with open(
        f"measurements/long_zmq_{io_length}/{number}_{kind}_results.txt", "r"
    ) as file:
        content = loads(file.read())
    avg_latency = []
    median_latency = []
    min_latency = []
    max_latency = []
    pstdev_latency = []
    length = len(content[0]["latency"])
    for number_query in range(length):
        query_latencys = [
            content[client]["latency"][number_query] for client in range(64)
        ]
        avg_latency.append(round(mean(query_latencys) / 1_000_000, 3))
        # median_latency.append(round(median(query_latencys)/ 1_000_000, 3))
        min_latency.append(round(min(query_latencys) / 1_000_000, 3))
        max_latency.append(round(max(query_latencys) / 1_000_000, 3))
        pstdev_latency.append(round(pstdev(query_latencys) / 1_000_000, 3))
    return {
        "avg_latency": avg_latency,
        # "median_latency": median_latency,
        "min_latency": min_latency,
        "max_latency": max_latency,
        "pstdev_latency": pstdev_latency,
    }


def get_total_latency(number, io_length, kind):
    with open(
        f"measurements/long_zmq_{io_length}/{number}_{kind}_results.txt", "r"
    ) as file:
        content = loads(file.read())
    return content


def plot_lines_clients(data, ax, s_range, e_range):
    for i in range(s_range, e_range, 4):
        values_smoothed_one = gaussian_filter1d(data[i]["latency"], sigma=150.0)
        values_smoothed_one = [round(val / 1_000_000, 3) for val in values_smoothed_one]
        values_smoothed_two = gaussian_filter1d(data[i + 1]["latency"], sigma=150.0)
        values_smoothed_two = [round(val / 1_000_000, 3) for val in values_smoothed_two]
        values_smoothed_three = gaussian_filter1d(data[i + 2]["latency"], sigma=150.0)
        values_smoothed_three = [
            round(val / 1_000_000, 3) for val in values_smoothed_three
        ]
        values_smoothed_four = gaussian_filter1d(data[i + 3]["latency"], sigma=150.0)
        values_smoothed_four = [
            round(val / 1_000_000, 3) for val in values_smoothed_four
        ]
        avg_values = []
        for z in range(len(values_smoothed_four)):
            avg_values.append(
                (
                    values_smoothed_one[z]
                    + values_smoothed_two[z]
                    + values_smoothed_three[z]
                    + values_smoothed_four[z]
                )
                / 4
            )
        ax.plot(
            avg_values, label=f"avg clients {i} to {i+3}", linewidth=4.0,
        )
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("query")


def plot_line_total(data, title, ax_1, ax_2, ax_3, ax_4):
    plot_lines_clients(data, ax_1, 0, 16)
    plot_lines_clients(data, ax_2, 16, 32)
    plot_lines_clients(data, ax_3, 32, 48)
    plot_lines_clients(data, ax_4, 48, 64)


def plot_line(data, title, ax):
    component_color = {
        "median_latency": "orange",
        "avg_latency": "blue",
        "min_latency": "darkgreen",
        "max_latency": "firebrick",
        "pstdev_latency": "darkorchid",
    }
    for latency_statistic, value in data.items():
        values_smoothed = gaussian_filter1d(value, sigma=20.0)
        ax.plot(
            values_smoothed,
            label=latency_statistic,
            linewidth=4.0,
            color=component_color[latency_statistic],
        )
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start + 781, end, 5000))
    ax.legend(loc="upper left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("query")
    ax.set_title(f"Latency {title}")
    ax.grid()


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
    widths = [20]
    hights = [10]
    spec = gridspec.GridSpec(
        ncols=1, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_latency_2_worker = fig.add_subplot(spec[0, 0])
    plot_line(get_latency(2, 1, "worker"), "2 processes", ax_latency_2_worker)
    fig.savefig("2_worker_1_latency.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(40, 20),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20, 20]
    hights = [10, 10]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_line_total(
        get_total_latency(2, 1, "worker"),
        "2 processes",
        ax_top_left,
        ax_top_right,
        ax_down_left,
        ax_down_right,
    )
    fig.savefig("total_2_worker_1_latency.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(40, 20),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [20, 20]
    hights = [10, 10]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_line_total(
        get_total_latency(128, 1, "worker"),
        "128 processes",
        ax_top_left,
        ax_top_right,
        ax_down_left,
        ax_down_right,
    )
    fig.savefig("total_128_worker_1_latency.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
