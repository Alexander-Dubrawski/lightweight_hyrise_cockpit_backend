# type: ignore
# flake8: noqa
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from .wsgi_results import (
    latency_threads_1,
    latency_threads_50,
    latency_threads_worker,
    latency_workers_1,
    latency_workers_50,
    throughput_threads_1,
    throughput_threads_50,
    throughput_threads_worker,
    throughput_workers_1,
    throughput_workers_50,
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


def plot_bar_latency(data, title, p_type, ax):
    quantities = [1, 2, 4, 8, 16, 32, 64]
    values = []
    max_value = 0
    for quan in quantities:
        values.append(data[quan]["50%"])
        if max_value < data[quan]["50%"]:
            max_value = data[quan]["50%"]
    ind = np.arange(len(quantities))
    width = 0.60
    if p_type == "Arbeiter-Threads":
        color = "darkorange"
    else:
        color = "steelblue"
    bar_chart = ax.bar(ind, values, width, label="", color=color)
    autolabel(bar_chart, ax)
    ax.legend()
    legend = ax.legend()
    legend.remove()
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    y_max = (max_value / 100) * 10
    ax.axis(ymin=0, ymax=(y_max + max_value))


def plot_line_hdr_histogramm_w_t(data, ax, ax_table):
    percentiles = [
        "1%",
        "10%",
        "20%",
        "30%",
        "40%",
        "50%",
        "60%",
        "70%",
        "80%",
        "90%",
        "99%",
        "99.9%",
        "99.99%",
    ]
    quantities = [
        (2, 32),
        (3, 32),
        (4, 32),
        (3, 16),
        (4, 16),
        (2, 64),
    ]
    component_color = {
        (1, 1): "red",
        (80, 1): "blue",
        (2, 32): "darkgreen",
        (3, 32): "firebrick",
        (4, 32): "darkorchid",
        (3, 16): "grey",
        (4, 16): "darkkhaki",
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


def plot_bar_w_t(data, ax, ax_table):
    quantities = [
        (2, 32),
        (3, 32),
        (4, 32),
        (3, 16),
        (4, 16),
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


def plot_line_hdr_histogramm(data, title, p_type, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%"]
    quantities = [1, 2, 4, 8, 16, 32, 64]
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
    ax.legend(loc="upper left", prop={"size": 15})
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Perzentil")
    ax.set_title(f"Latenz nach Perzentilverteilung {title}")
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


def plot_line_hdr_histogramm_cut(data, title, p_type, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%"]
    quantities = [1, 2, 4, 8, 16, 32, 64]
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
    ax.legend(loc="upper left", prop={"size": 15})
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Perzentil")
    ax.set_title(f"Latenz nach Perzentilverteilung {title}")
    ax.grid()
    ax.axis(ymin=0, ymax=(2800))
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


def plot_bar(data, title, p_type, ax, ymax=None):
    quantities = [1, 2, 4, 8, 16, 32, 64]
    values = []
    max_value = 0
    for quan in quantities:
        values.append(data[quan])
        if max_value < data[quan]:
            max_value = data[quan]
    ind = np.arange(len(quantities))
    width = 0.60
    if p_type == "Arbeiter-Threads":
        color = "darkorange"
    else:
        color = "steelblue"
    bar_chart = ax.bar(ind, values, width, label="Anfragen / Sek.", color=color)
    autolabel(bar_chart, ax)
    legend = ax.legend()
    legend.remove()
    ax.set_ylabel("Anfragen / Sek.")
    ax.set_xlabel(p_type)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(quantities)
    if ymax is None:
        y_max = ((max_value / 100) * 10) + max_value
    else:
        y_max = ymax
    ax.axis(ymin=0, ymax=(y_max))
    # ax_table.axis("tight")
    # ax_table.axis("off")
    # table = ax_table.table(
    #     cellText=[["%06.2f" % val for val in values]],
    #     rowLabels=["AVG"],
    #     cellLoc="center",
    #     colLabels=quantities,
    #     loc="center",
    # )
    # table.scale(1, 2)
    # table.set_fontsize(30)


def main():
    plt.rcParams.update({"font.size": 18})
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
        "Arbeiter-Threads (I/O 1 ms)",
        "Arbeiter-Threads",
        ax_latency_threads,
        ax_latency_threads_table,
    )
    plot_line_hdr_histogramm_cut(
        latency_workers_1,
        "Arbeiter-Prozesse (I/O 1 ms)",
        "Arbeiter-Prozesse",
        ax_latency_worker,
        ax_latency_worker_table,
    )

    fig.savefig("wsgi_latency_1.pdf")
    plt.close(fig)

    # plt.rcParams.update({"font.size": 20})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(20, 10),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [10, 10]
    # hights = [7, 3]
    # spec = gridspec.GridSpec(
    #     ncols=2, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_latency_threads = fig.add_subplot(spec[0, 0])
    # ax_latency_threads_table = fig.add_subplot(spec[1, 0])
    # ax_latency_worker = fig.add_subplot(spec[0, 1])
    # ax_latency_worker_table = fig.add_subplot(spec[1, 1])

    # plot_line_hdr_histogramm(
    #     latency_threads_50,
    #     "threads (I/O 50ms)",
    #     "threads",
    #     ax_latency_threads,
    #     ax_latency_threads_table,
    # )
    # plot_line_hdr_histogramm(
    #     latency_workers_50,
    #     "processes (I/O 50ms)",
    #     "processes",
    #     ax_latency_worker,
    #     ax_latency_worker_table,
    # )

    # fig.savefig("wsgi_latency_50.pdf")
    # plt.close(fig)

    plt.rcParams.update({"font.size": 9})
    fig = plt.figure(
        num=None,
        figsize=(10, 3),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [5, 5]
    hights = [3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput_threads = fig.add_subplot(spec[0, 0])
    # ax_throughput_threads_table = fig.add_subplot(spec[1, 0])
    ax_throughput_worker = fig.add_subplot(spec[0, 1])
    # ax_throughput_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_threads_1,
        "Durchsatz Arbeiter-Threads (I/O 1 ms)",
        "Arbeiter-Threads",
        ax_throughput_threads,
        ymax=212
        # ax_throughput_threads_table,
    )
    plot_bar(
        throughput_workers_1,
        "Durchsatz Arbeiter-Prozesse (I/O 1 ms)",
        "Arbeiter-Prozesse",
        ax_throughput_worker,
        ymax=212
        # ax_throughput_worker_table,
    )

    fig.savefig("wsgi_throughput_1.pdf")
    plt.close(fig)

    plt.rcParams.update({"font.size": 9})
    fig = plt.figure(
        num=None,
        figsize=(10, 3),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [5, 5]
    hights = [3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_throughput_threads = fig.add_subplot(spec[0, 0])
    # ax_throughput_threads_table = fig.add_subplot(spec[1, 0])
    ax_throughput_worker = fig.add_subplot(spec[0, 1])
    # ax_throughput_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_threads_50,
        "Durchsatz Arbeiter-Threads (I/O 50 ms)",
        "Arbeiter-Threads",
        ax_throughput_threads,
        ymax=21
        # ax_throughput_threads_table,
    )
    plot_bar(
        throughput_workers_50,
        "Durchsatz Arbeiter-Prozesse (I/O 50 ms)",
        "Arbeiter-Prozesse",
        ax_throughput_worker,
        ymax=21
        # ax_throughput_worker_table,
    )

    fig.savefig("wsgi_throughput_50.pdf")
    plt.close(fig)

    # fig.savefig("wsgi_throughput_50.pdf")
    # plt.close(fig)

    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(15, 8),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [15]
    hights = [5, 3]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_latency = fig.add_subplot(spec[0, 0])
    ax_latency_table = fig.add_subplot(spec[1, 0])
    # ax_throughput = fig.add_subplot(spec[0, 1])
    # ax_throughput_table = fig.add_subplot(spec[1, 1])

    plot_line_hdr_histogramm_w_t(latency_threads_worker, ax_latency, ax_latency_table)
    # plot_bar_w_t(throughput_threads_worker, ax_throughput, ax_throughput_table)

    fig.savefig("wsgi_combi_latency_50.pdf")
    plt.close(fig)

    # plt.rcParams.update({"font.size": 22})
    # fig = plt.figure(
    #     num=None,
    #     figsize=(12, 6),
    #     dpi=300,
    #     facecolor="w",
    #     edgecolor="k",
    #     constrained_layout=True,
    # )
    # widths = [12]
    # hights = [5, 1]
    # spec = gridspec.GridSpec(
    #     ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_throughput = fig.add_subplot(spec[0, 0])
    # ax_throughput_table = fig.add_subplot(spec[1, 0])
    # plot_bar_w_t(throughput_threads_worker, ax_throughput, ax_throughput_table)
    # fig.savefig("wsgi_combi_throughput_50.pdf")
    # plt.close(fig)

    plt.rcParams.update({"font.size": 9})
    fig = plt.figure(
        num=None,
        figsize=(10, 3),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [5, 5]
    hights = [3]
    spec = gridspec.GridSpec(
        ncols=2, nrows=1, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_latency_threads = fig.add_subplot(spec[0, 0])
    # ax_throughput_threads_table = fig.add_subplot(spec[1, 0])
    ax_latency_worker = fig.add_subplot(spec[0, 1])
    # ax_throughput_worker_table = fig.add_subplot(spec[1, 1])

    plot_bar_latency(
        latency_threads_50,
        "Latenz Arbeiter-Threads (I/O 50 ms)",
        "Arbeiter-Threads",
        ax_latency_threads,
        #       ax_latency_threads_table,
    )
    plot_bar_latency(
        latency_workers_50,
        "Latenz Arbeiter-Prozesse (I/O 50 ms)",
        "Arbeiter-Prozesse",
        ax_latency_worker,
        #        ax_latency_worker_table,
    )

    fig.savefig("wsgi_bar_latency_50.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
