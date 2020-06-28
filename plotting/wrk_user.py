# type: ignore
# flake8: noqa
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np

from .wrk_user_results import (
    avg_latency_flask,
    avg_latency_manager,
    latency_flask,
    latency_manager,
    throughput_flask,
    throughput_manager,
)

# import locale
# # Set to German locale to get comma decimal separater
# locale.setlocale(locale.LC_NUMERIC, "de_DE")


# def plot_linear_dependency_throughput(data_flask, data_manager, ax, ax_table):
#     number_clients = [1, 2, 4, 8, 16, 32, 64]
#     ax.plot(
#         list(data_flask.keys()),
#         list(data_flask.values()),
#         label=f"Anfragen/Sek. flask_metric",
#         linewidth=4.0,
#         color="orange",
#         )
#     ax.plot(
#         list(data_manager.keys()),
#         list(data_manager.values()),
#         label=f"Anfragen/Sek manager_metric",
#         linewidth=4.0,
#         color="blue",
#         )
#     ax.legend(loc='upper right')
#     ax.set_ylabel("Anfragen/Sek")
#     ax.set_xlabel("Klienten")
#     ax.set_title("Durchsatz")
#     table = ax_table.table(
#         cellText=[list(data_flask.values()), list(data_manager.values())],
#         rowLabels=["AVG flask_metric", "AVG manager_metric"],
#         cellLoc="center",
#         colLabels=list(data_manager.keys()),
#         loc="center",
#     )
def func(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    ind = s.index(".")
    return s[:ind] + "," + s[ind + 1 :]  # change dot to comma


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            "{}".format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )


def plot_line_hdr_histogramm(data, title, ax):
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
    ax.set_ylabel("Latenz (Millisekunden)")
    ax.set_xlabel("Perzentil")
    ax.set_title(f"Latenz nach Perzentilverteilung {title}")
    ax.grid()
    y_format = tkr.FuncFormatter(func)
    ax.yaxis.set_major_formatter(y_format)
    # ax_table.axis("tight")
    # ax_table.axis("off")
    # table = ax_table.table(
    #     cellText=rows,
    #     rowLabels=row_labels,
    #     cellLoc="center",
    #     colLabels=percentiles,
    #     loc="center",
    # )
    # table.scale(1, 3)


def plot_bar(data, title, ax, ylable, ymax=None):
    number_clients = [1, 2, 4, 8, 16, 32, 64]
    values = []
    max_value = 0
    for number_client in number_clients:
        values.append(data[number_client])
        if max_value < data[number_client]:
            max_value = data[number_client]
    ind = np.arange(len(number_clients))
    width = 0.60
    bar_chart = ax.bar(ind, values, width, label="Anfragen / Sek")
    # ax.plot(
    #     np.arange(len(number_clients)),
    #     values,
    #     'o-',
    #     label=f"Anfragen/Sek",
    #     linewidth=4.0,
    #     color="orange",
    #     )
    autolabel(bar_chart, ax)
    legend = ax.legend()
    legend.remove()
    ax.set_ylabel(ylable)
    ax.set_xlabel("Klienten")
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(number_clients)
    if ymax is None:
        y_max = ((max_value / 100) * 10) + max_value
    else:
        y_max = ymax
    ax.axis(ymin=0, ymax=y_max)
    # ax_table.axis("tight")
    # ax_table.axis("off")
    # table = ax_table.table(
    #     cellText=[["%04.1f" % val for val in values]],
    #     rowLabels=["i. D."],
    #     cellLoc="center",
    #     colLabels=number_clients,
    #     loc="center",
    # )
    # table.scale(1, 2)
    # table.set_fontsize(30)


def main():
    plt.rcParams.update({"font.size": 9})
    # plt.rcParams['axes.formatter.use_locale'] = True
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
    ax_io_flask_throughput = fig.add_subplot(spec[0, 0])
    # ax_io_flask_throughput_table = fig.add_subplot(spec[1, 0])
    ax_io_manager_throughput = fig.add_subplot(spec[0, 1])
    # ax_io_manager_throughput_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        throughput_flask,
        "Durchsatz flask_metric",
        ax_io_flask_throughput,
        # ax_io_flask_throughput_table,
        "Anfragen / Sek.",
        ymax=22,
    )
    plot_bar(
        throughput_manager,
        "Durchsatz manager_metric",
        ax_io_manager_throughput,
        # ax_io_manager_throughput_table,
        "Anfragen / Sek.",
        ymax=22,
    )
    fig.savefig("user_wrk_throughput.pdf")
    plt.close(fig)

    # plt.rcParams.update({"font.size": 22})
    # plt.rcParams['axes.formatter.use_locale'] = True
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
    ax_io_flask_latency = fig.add_subplot(spec[0, 0])
    # ax_io_flask_latency_table = fig.add_subplot(spec[1, 0])
    ax_io_manager_latency = fig.add_subplot(spec[0, 1])
    # ax_io_manager_latency_table = fig.add_subplot(spec[1, 1])

    plot_bar(
        avg_latency_flask,
        "Latenz flask_metric",
        ax_io_flask_latency,
        # ax_io_flask_latency_table,
        "Latenz (Millisekunden)",
        ymax=3900,
    )
    plot_bar(
        avg_latency_manager,
        "Latenz manager_metric",
        ax_io_manager_latency,
        # ax_io_manager_latency_table,
        "Latenz (Millisekunden)",
        ymax=3900,
    )
    fig.savefig("user_wrk_latency.pdf")
    plt.close(fig)

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
    # hights = [7, 3]
    # spec = gridspec.GridSpec(
    #     ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    # )
    # ax_top_left = fig.add_subplot(spec[0, 0])
    # ax_down_left = fig.add_subplot(spec[1, 0])

    # plot_linear_dependency_throughput(throughput_flask, throughput_manager, ax_top_left, ax_down_left)
    # fig.savefig("throughput_before.pdf")
    # plt.close(fig)


if __name__ == "__main__":
    main()
