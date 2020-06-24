# type: ignore
# flake8: noqa
from json import loads
from statistics import mean, median, pstdev, stdev

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.ndimage.filters import gaussian_filter1d


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            "{}".format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 0),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )


def get_latency(number, io_length, kind, broker_type):
    with open(
        f"measurements/detailed_long_zmq_{io_length}_{broker_type}/{number}_{kind}_results.txt",
        "r",
    ) as file:
        content = loads(file.read())
    avg_latency = []
    median_latency = []
    min_latency = []
    max_latency = []
    pstdev_latency = []
    length = 150_000
    for number_query in range(10, length):
        query_latencys = [
            content[client]["latency"][number_query] for client in range(64)
        ]
        # avg_latency.append(round(mean(query_latencys) / 1_000_000, 3))
        # median_latency.append(round(median(query_latencys)/ 1_000_000, 3))
        # min_latency.append(round(min(query_latencys) / 1_000_000, 3))
        # max_latency.append(round(max(query_latencys) / 1_000_000, 3))
        pstdev_latency.append(round(stdev(query_latencys) / 1_000_000, 3))
    return {
        # "avg_latency": avg_latency,
        # "median_latency": median_latency,
        # "min_latency": min_latency,
        # "max_latency": max_latency,
        "Standardabweichung": pstdev_latency,
    }


def get_total_latency(number, io_length, kind, broker_type):
    with open(
        f"measurements/detailed_long_zmq_{io_length}_{broker_type}/{number}_{kind}_results.txt",
        "r",
    ) as file:
        content = loads(file.read())
    return content


def get_avg_latency(number, io_length, kind, broker_type):
    with open(
        f"measurements/detailed_long_zmq_{io_length}_{broker_type}/{number}_{kind}_results_formatted.txt",
        "r",
    ) as file:
        content = loads(file.read())
    return content["64"]["Avg"]


def get_avg_clients(data, index, number_clients, sigma):
    values_smoothed = []
    for i in range(number_clients):
        length = len(data[index + i]["latency"])
        stdev_latency = []
        for number_query in range(0, length, 1000):
            stdev_latency.append(
                round(
                    stdev(
                        data[index + i]["latency"][number_query : number_query + 1000]
                    )
                    / 1_000_000,
                    3,
                )
            )
        # values_smoothed.append(
        #     [
        #         round(val / 1_000_000, 3)
        #         for val in gaussian_filter1d(data[index + i]["latency"], sigma=sigma)
        #     ]
        # )
        values_smoothed.append(stdev_latency)
    avg_values = []
    for i in range(len(values_smoothed[0])):
        avg_value = 0
        for z in values_smoothed:
            avg_value += z[i]
        avg_values.append(avg_value / number_clients)
    return avg_values


def plot_lines_clients(data, ax, s_range, e_range, number_clients, sigma):
    for i in range(s_range, e_range, number_clients):
        avg_values = get_avg_clients(data, i, number_clients, sigma)
        ax.plot(
            avg_values, label=f"avg clients {i} to {i+number_clients}", linewidth=4.0,
        )
    ax.legend(loc="lower left")
    ax.set_ylabel("Latency (milliseconds)")
    ax.set_xlabel("query")


def plot_line_total(data, title, ax_1, ax_2, ax_3, ax_4):
    plot_lines_clients(data, ax_1, 0, 16, 4, 1500)
    plot_lines_clients(data, ax_2, 16, 32, 4, 1500)
    plot_lines_clients(data, ax_3, 32, 48, 4, 1500)
    plot_lines_clients(data, ax_4, 48, 64, 4, 1500)


def plot_line_total_split(data, title, ax_1, ax_2):
    plot_lines_clients(data, ax_1, 0, 32, 8, 750)
    plot_lines_clients(data, ax_2, 32, 64, 8, 750)


def plot_line_total_single(data_balanced, data_not_balanced, ax):
    avg_values = get_avg_clients(data_balanced, 0, 64, 1000)
    ax.plot(
        avg_values,
        label=f"Standardabweichung balanciert",
        linewidth=4.0,
        color="steelblue",
    )
    avg_values = get_avg_clients(data_not_balanced, 0, 64, 1000)
    ax.plot(
        avg_values,
        label=f"Standardabweichung nicht balanciert",
        linewidth=4.0,
        color="orange",
    )
    ax.get_xaxis().set_major_formatter(
        FuncFormatter(lambda x, p: format(int(x) * 1000, ","))
    )
    ax.legend(prop={"size": 13})
    ax.set_title("Latenz Standardabweichung")
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Anfragen")


def plot_line(data_balanced, data_not_balanced, title, ax):
    component_color = {
        "median_latency": "orange",
        "avg_latency": "blue",
        "min_latency": "darkgreen",
        "max_latency": "firebrick",
        "Standardabweichung": "orange",
    }
    for latency_statistic, value in data_balanced.items():
        values_smoothed = gaussian_filter1d(value, sigma=300.0)
        ax.plot(
            values_smoothed,
            label="Standardabweichung balanciert",
            linewidth=4.0,
            color="steelblue",
        )
    for latency_statistic, value in data_not_balanced.items():
        values_smoothed = gaussian_filter1d(value, sigma=300.0)
        ax.plot(
            values_smoothed,
            label="Standardabweichung nicht balanciert",
            linewidth=4.0,
            color="orange",
        )
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start + 781, end, 5000))
    ax.legend(loc="upper left", prop={"size": 13})
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Anfragen")
    ax.set_title(f"Latenz {title}")
    ax.axis(xmin=0, xmax=150_000)
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))
    ax.grid()


def plot_bar_latency(data_balanced, data_not_balanced, ax):
    values = []
    max_value = data_balanced
    if max_value < data_not_balanced:
        max_value = data_not_balanced
    ind = np.arange(len([data_balanced]))
    width = 0.10
    bar_chart_balanced = ax.bar(
        ind - width / 2,
        [data_balanced],
        width,
        color="steelblue",
        label="Latenz i. D. balanciert",
    )
    bar_chart_not_balanced = ax.bar(
        ind + width / 2,
        [data_not_balanced],
        width,
        color="orange",
        label="Latenz i. D. nicht balanciert",
    )
    autolabel(bar_chart_balanced, ax)
    autolabel(bar_chart_not_balanced, ax)
    ax.legend(prop={"size": 13})
    ax.set_xlabel("Prozesse")
    ax.set_xticks(ind)
    ax.set_xticklabels([2])
    ax.set_ylabel("Anfragen / Sek.")
    ax.set_title("Latenz i. D.")
    y_max = (max_value / 100) * 20
    ax.axis(ymin=0, ymax=(y_max + max_value))


def main():

    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(20, 10),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [20]
    # hights = [10]
    # spec = gridspec.GridSpec(
    #     ncols=1, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_latency_2_worker = fig.add_subplot(spec[0, 0])
    # plot_line(get_latency(2, 1, "worker", "balanced"),get_latency(2, 1, "worker", "not_balanced"), "2 Prozesse", ax_latency_2_worker)
    # fig.savefig("2_worker_1_latency.pdf")
    # plt.close(fig)

    # print("Plotting total_2_worker_1_latency")
    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(40, 20),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [20, 20]
    # hights = [10, 10]
    # spec = gridspec.GridSpec(
    #     ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_top_right = fig.add_subplot(spec[0, 1])
    # ax_down_left = fig.add_subplot(spec[1, 0])
    # ax_down_right = fig.add_subplot(spec[1, 1])
    # plot_line_total(
    #     get_total_latency(2, 1, "worker", "not_balanced"),
    #     "2 processes",
    #     ax_top_left,
    #     ax_top_right,
    #     ax_down_left,
    #     ax_down_right,
    # )
    # fig.savefig("total_2_worker_1_latency.pdf")
    # plt.close(fig)

    print("Plotting total_2_worker_1_latency_single")
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(18, 8),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [14, 4]
    hights = [8]
    spec = gridspec.GridSpec(
        ncols=2, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    plot_bar_latency(
        get_avg_latency(2, 1, "worker", "balanced"),
        get_avg_latency(2, 1, "worker", "not_balanced"),
        ax_top_right,
    )
    plot_line_total_single(
        get_total_latency(2, 1, "worker", "balanced"),
        get_total_latency(2, 1, "worker", "not_balanced"),
        ax_top_left,
    )
    fig.savefig("total_2_worker_1_latency_single.pdf")
    plt.close(fig)

    print("Plotting total_32_worker_50_latency_single")
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(18, 8),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [14, 4]
    hights = [8]
    spec = gridspec.GridSpec(
        ncols=2, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    plot_bar_latency(
        get_avg_latency(32, 50, "worker", "balanced"),
        get_avg_latency(32, 50, "worker", "not_balanced"),
        ax_top_right,
    )
    plot_line_total_single(
        get_total_latency(32, 50, "worker", "balanced"),
        get_total_latency(32, 50, "worker", "not_balanced"),
        ax_top_left,
    )
    fig.savefig("total_32_worker_50_latency_single.pdf")
    plt.close(fig)
    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(40, 20),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [20, 20]
    # hights = [10, 10]
    # spec = gridspec.GridSpec(
    #     ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_top_right = fig.add_subplot(spec[0, 1])
    # ax_down_left = fig.add_subplot(spec[1, 0])
    # ax_down_right = fig.add_subplot(spec[1, 1])
    # print("total_128_worker_1_latency.pdf")

    # plot_line_total(
    #     get_total_latency(128, 1, "worker", "balanced"),
    #     "128 processes",
    #     ax_top_left,
    #     ax_top_right,
    #     ax_down_left,
    #     ax_down_right,
    # )
    # fig.savefig("total_128_worker_1_latency.pdf")
    # plt.close(fig)

    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(40, 20),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [40]
    # hights = [10, 10]
    # spec = gridspec.GridSpec(
    #     ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )

    # print("Plotting split_total_2_worker_1_latency.pdf")
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_down_left = fig.add_subplot(spec[1, 0])
    # plot_line_total_split(
    #     get_total_latency(2, 1, "worker", "balanced"), "2 processes", ax_top_left, ax_down_left
    # )
    # fig.savefig("split_total_2_worker_1_latency.pdf")
    # plt.close(fig)


if __name__ == "__main__":
    main()
