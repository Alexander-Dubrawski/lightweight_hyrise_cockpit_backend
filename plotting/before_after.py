# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .wrk_user_results import (
    avg_latency_flask,
    avg_latency_manager,
    throughput_flask,
    throughput_manager,
)
from .wrk_user_results_after import (
    avg_latency_flask_after,
    avg_latency_manager_after,
    throughput_flask_after,
    throughput_manager_after,
)


def plot_bar_latency(data_before, data_after, endpoint, ax, ax_table):
    quantities = [1, 2, 4, 8, 16, 32, 64]
    before_values = []
    after_values = []
    max_value = 0
    for quan in quantities:
        before_values.append(data_before[quan])
        if max_value < data_before[quan]:
            max_value = data_before[quan]
        after_values.append(data_after[quan])
        if max_value < data_after[quan]:
            max_value = data_after[quan]
    ind = np.arange(len(quantities))
    width = 0.30
    ax.bar(
        ind - width / 2,
        before_values,
        width,
        label="befor Optimierung",
        color="steelblue",
    )
    ax.bar(
        ind + width / 2, after_values, width, label="nach Optimierung", color="orange",
    )
    ax.legend(prop={"size": 13}, loc="upper left")
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Klienten")
    ax.set_title(f"Latenz bevor und nach Optimierung {endpoint}")
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    y_max = (max_value / 100) * 20
    ax.axis(ymin=0, ymax=(y_max + max_value))
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[
            ["%08.3f" % val for val in before_values],
            ["%08.3f" % val for val in after_values],
        ],
        rowLabels=["bevor", "nach"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(25)


def plot_bar_throughput(data_before, data_after, endpoint, ax, ax_table):
    quantities = [1, 2, 4, 8, 16, 32, 64]
    before_values = []
    after_values = []
    max_value = 0
    for quan in quantities:
        before_values.append(data_before[quan])
        if max_value < data_before[quan]:
            max_value = data_before[quan]
        after_values.append(data_after[quan])
        if max_value < data_after[quan]:
            max_value = data_after[quan]
    ind = np.arange(len(quantities))
    width = 0.30
    ax.bar(
        ind - width / 2,
        before_values,
        width,
        label="bevor Optimierung",
        color="steelblue",
    )
    ax.bar(
        ind + width / 2, after_values, width, label="nach Optimierung", color="orange",
    )
    ax.legend(prop={"size": 13}, loc="upper left")
    ax.set_ylabel("Anfragen / Sek.")
    ax.set_xlabel("Klienten")
    ax.set_title(f"Durchsatz bevor und nach Optimierung {endpoint}")
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    y_max = (max_value / 100) * 25
    ax.axis(ymin=0, ymax=(y_max + max_value))
    ax_table.axis("tight")
    ax_table.axis("off")
    table = ax_table.table(
        cellText=[
            ["%05.2f" % val for val in before_values],
            ["%05.2f" % val for val in after_values],
        ],
        rowLabels=["bevor", "nach"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(12)


def plot_line_hdr_histogramm(data, title, ax, ax_table):
    percentiles = ["1%", "25%", "50%", "75%", "90%", "99%", "99.9%", "99.99%"]
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
    table.set_fontsize(25)


def main():
    plt.rcParams.update({"font.size": 19})
    fig = plt.figure(
        num=None,
        figsize=(20, 7),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10, 10]
    hights = [5, 2]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_throughput(
        throughput_flask,
        throughput_flask_after,
        "flask_metric",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        avg_latency_flask,
        avg_latency_flask_after,
        "flask_metric",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("before_after_flask_metric.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 19})
    fig = plt.figure(
        num=None,
        figsize=(20, 7),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10, 10]
    hights = [5, 2]
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_top_right = fig.add_subplot(spec[0, 1])
    ax_down_left = fig.add_subplot(spec[1, 0])
    ax_down_right = fig.add_subplot(spec[1, 1])
    plot_bar_throughput(
        throughput_manager,
        throughput_manager_after,
        "manager_metric",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        avg_latency_manager,
        avg_latency_manager_after,
        "manager_metric",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("before_after_manager_metric.pdf")
    plt.close(fig)

    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(30, 15),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [15, 15]
    # hights = [10, 5]
    # spec = gridspec.GridSpec(
    #     ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_top_right = fig.add_subplot(spec[0, 1])
    # ax_down_left = fig.add_subplot(spec[1, 0])
    # ax_down_right = fig.add_subplot(spec[1, 1])
    # plot_line_hdr_histogramm(
    #     latency_flask, "flask_metric before", ax_top_left, ax_down_left
    # )
    # plot_line_hdr_histogramm(
    #     latency_flask_after, "flask_metric after", ax_top_right, ax_down_right
    # )
    # fig.savefig("before_after_flask_latency.pdf")
    # plt.close(fig)

    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(30, 15),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [15, 15]
    # hights = [10, 5]
    # spec = gridspec.GridSpec(
    #     ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_top_right = fig.add_subplot(spec[0, 1])
    # ax_down_left = fig.add_subplot(spec[1, 0])
    # ax_down_right = fig.add_subplot(spec[1, 1])
    # plot_line_hdr_histogramm(
    #     latency_manager, "manager_metric before", ax_top_left, ax_down_left
    # )
    # plot_line_hdr_histogramm(
    #     latency_manager_after, "manager_metric after", ax_top_right, ax_down_right
    # )
    # fig.savefig("before_after_manager_latency.pdf")
    # plt.close(fig)


if __name__ == "__main__":
    main()
