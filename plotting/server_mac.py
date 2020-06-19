# type: ignore
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

server_latency = {
    "1%": 2.305,
    "25%": 2.403,
    "50%": 2.438,
    "75%": 2.461,
    "90%": 2.476,
    "99%": 2.511,
    "99.9%": 2.953,
    "99.99%": 3.265,
}
mac_latency = {
    "1%": 2.457,
    "25%": 2.819,
    "50%": 2.904,
    "75%": 3.029,
    "90%": 3.149,
    "99%": 72.178,
    "99.9%": 646.724,
    "99.99%": 916.441,
}


def plot_line_hdr_histogramm(mac_data, server_data, ax, ax_table):
    percentiles = ["1%", "50%", "99%", "99.9%", "99.99%"]
    row_labels = []
    rows = []
    y_values = []
    row = []
    row_labels.append("MacBookPro & MacOS 10.15.5")
    for percentile in percentiles:
        y_values.append(mac_data[percentile])
        row.append(mac_data[percentile])
    rows.append(["%07.3f" % val for val in row])
    ax.plot(
        percentiles, y_values, label="MacBookPro & MacOS 10.15.5", linewidth=4.0,
    )
    y_values = []
    row = []
    row_labels.append("Server & Ubuntu 20.04 LTS")
    for percentile in percentiles:
        y_values.append(server_data[percentile])
        row.append(server_data[percentile])
    rows.append(["%07.3f" % val for val in row])
    ax.plot(
        percentiles, y_values, label="Server & Ubuntu 20.04 LTS", linewidth=4.0,
    )
    ax.legend(loc="upper left")
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
        colLabels=percentiles,
        loc="center",
    )
    table.scale(1, 3)


def main():
    plt.rcParams.update({"font.size": 22})
    fig = plt.figure(
        num=None,
        figsize=(20, 8),
        dpi=300,
        facecolor="w",
        edgecolor="k",
        constrained_layout=True,
    )
    widths = [10]
    hights = [6, 2]
    spec = gridspec.GridSpec(
        ncols=1, nrows=2, figure=fig, width_ratios=widths, height_ratios=hights
    )
    ax_io_latency = fig.add_subplot(spec[0, 0])
    ax_io_latency_table = fig.add_subplot(spec[1, 0])
    plot_line_hdr_histogramm(
        mac_latency, server_latency, ax_io_latency, ax_io_latency_table
    )
    fig.savefig("mac_server_latency.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
