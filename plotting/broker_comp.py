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
    width = 0.30
    if p_type == "Arbeiter-Threads":
        no_balance_color = "orange"
        balance_color = "firebrick"
    else:
        no_balance_color = "steelblue"
        balance_color = "forestgreen"
    ax.bar(
        ind - width / 2,
        balance_values,
        width,
        label="Latenz i. D. balanciert",
        color=balance_color,
    )
    ax.bar(
        ind + width / 2,
        no_balance_value,
        width,
        label="Latenz i. D. nicht balanciert",
        color=no_balance_color,
    )
    ax.legend(prop={"size": 15})
    ax.set_ylabel("Latenz (Millisekunden)")
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
        rowLabels=["balanciert", "nicht balanciert"],
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
    width = 0.30
    if p_type == "Arbeiter-Threads":
        no_balance_color = "orange"
        balance_color = "firebrick"
    else:
        no_balance_color = "steelblue"
        balance_color = "forestgreen"
    ax.bar(
        ind - width / 2,
        balance_values,
        width,
        label="Anfragen / Sek. balanciert",
        color=balance_color,
    )
    ax.bar(
        ind + width / 2,
        no_balance_value,
        width,
        label="Anfragen / Sek. nicht balanciert",
        color=no_balance_color,
    )
    ax.legend(prop={"size": 15})
    ax.set_ylabel("Anfragen / Sek.")
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
        rowLabels=["balanciert", "nicht balanciert"],
        cellLoc="center",
        colLabels=quantities,
        loc="center",
    )
    table.scale(1, 2)
    table.set_fontsize(30)


def plot_bar_throughput_broker_comp(data_broker, data_balance, title, p_type, ax):
    quantities = [16, 32, 64]
    balance_values = []
    no_balance_value = []
    max_value = 0
    for quan in quantities:
        balance_values.append(round(data_balance[quan][0], 3))
        if max_value < data_balance[quan][0]:
            max_value = data_balance[quan][0]
        no_balance_value.append(round(data_broker[quan][0], 3))
        if max_value < data_broker[quan][0]:
            max_value = data_broker[quan][0]
    ind = np.arange(len(quantities))
    width = 0.30
    if p_type == "Arbeiter-Threads":
        no_balance_color = "orange"
        balance_color = "firebrick"
    else:
        no_balance_color = "steelblue"
        balance_color = "forestgreen"
    bar_balanced = ax.bar(
        ind - width / 2,
        balance_values,
        width,
        label="Anfragen / Sek. balanciert",
        color=balance_color,
    )
    bar_not_balanced = ax.bar(
        ind + width / 2,
        no_balance_value,
        width,
        label="Anfragen / Sek. nicht balanciert",
        color=no_balance_color,
    )
    autolabel(bar_balanced, ax)
    autolabel(bar_not_balanced, ax)
    ax.legend(loc="upper left", prop={"size": 11})
    ax.set_ylabel("Anfragen / Sek.")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    y_max = (max_value / 100) * 10
    ax.axis(ymin=0, ymax=(y_max + max_value))


def plot_line_hdr_histogramm(data_broker, data_balance, title, p_type, ax, ax_table):
    percentiles = ["1%", "50%", "90%", "99%", "99.9%", "99.99%", "99.999%"]
    component_color = {
        16: "orange",
        32: "blue",
        64: "firebrick",
    }
    quantities = [16, 32, 64]
    row_labels = []
    rows = []
    for quan in quantities:
        row_labels.append(f"balanciert {quan}")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data_balance[quan][0][percentile])
            row.append(data_balance[quan][0][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan} balanciert",
            linewidth=4.0,
            color=component_color[quan],
            linestyle="-",
        )
        row_labels.append(f"nicht balanciert {quan}")
        y_values = []
        row = []
        for percentile in percentiles:
            y_values.append(data_broker[quan][0][percentile])
            row.append(data_broker[quan][0][percentile])
        rows.append(["%08.3f" % val for val in row])
        ax.plot(
            percentiles,
            y_values,
            label=f"{p_type} {quan} nicht balanciert",
            linewidth=4.0,
            color=component_color[quan],
            linestyle="--",
        )
    ax.legend(loc="upper left", prop={"size": 15})
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Perzentil")
    ax.set_title("Latenz nach Perzentilverteilung")
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
        "Arbeiter-Threads (I/O 1 ms)",
        "Arbeiter-Threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        latency_workers_not_balanced_1,
        latency_workers_balanced_1,
        "Arbeiter-Prozesse (I/O 1 ms)",
        "Arbeiter-Prozesse",
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
        "Arbeiter-Threads (I/O 1 ms)",
        "Arbeiter-Threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_throughput(
        throughput_workers_not_balanced_1,
        throughput_workers_balanced_1,
        "Arbeiter-Prozesse (I/O 1 ms)",
        "Arbeiter-Prozesse",
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
        "Arbeiter-Threads (I/O 50 ms)",
        "Arbeiter-Threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_latency(
        latency_workers_not_balanced_50,
        latency_workers_balanced_50,
        "Arbeiter-Prozesse (I/O 50 ms)",
        "Arbeiter-Prozesse",
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
        "Arbeiter-Threads (I/O 50 ms)",
        "Arbeiter-Threads",
        ax_top_left,
        ax_down_left,
    )
    plot_bar_throughput(
        throughput_workers_not_balanced_50,
        throughput_workers_balanced_50,
        "Arbeiter-Prozesse (I/O 50 ms)",
        "Arbeiter-Prozesse",
        ax_top_right,
        ax_down_right,
    )
    fig.savefig("comp_throughput_broker_50.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(12, 5),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [12]
    hights = [5]
    spec = gridspec.GridSpec(
        ncols=1, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    plot_bar_throughput_broker_comp(
        throughput_workers_not_balanced_slow,
        throughput_workers_balanced_slow,
        "Durchsatz",
        "Arbeiter-Prozesse",
        ax_top_left,
    )
    fig.savefig("comp_slow_worker_throughput_broker.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(15, 9),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [15]
    hights = [6, 3]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_top_left = fig.add_subplot(spec[0, 0])
    ax_down_left = fig.add_subplot(spec[1, 0])
    plot_line_hdr_histogramm(
        latency_workers_not_balanced_slow,
        latency_workers_balanced_slow,
        "Latenz",
        "Arbeiter-Prozesse",
        ax_top_left,
        ax_down_left,
    )
    fig.savefig("comp_slow_worker_latency_broker.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
