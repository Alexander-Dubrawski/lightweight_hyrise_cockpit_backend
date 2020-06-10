import matplotlib.pyplot as plt
from matplotlib import ticker

colors = {
    "running on\nVM & Ubuntu 20.04 LTS\nfor 4m": "blue",
    "running on\nMacBookPro & MacOS 10.15.4\nfor 4m": "orange",
}


def plot_matrix_sub_plot(ax, row_labels, rows, col_labels):
    ax.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)


def plot_hdr_histogram(data, file_name):
    # fig = figure(num=None, figsize=(30, 10), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    fig, ax1 = plt.subplots(
        1, 1, figsize=(30, 10), dpi=300, facecolor="w", edgecolor="k"
    )
    col_labels = list(data["running on\nVM & Ubuntu 20.04 LTS\nfor 4m"].keys())
    rows = []
    row_labels = []
    for running_time, results in data.items():
        if running_time == "running on\nVM & Ubuntu 20.04 LTS\nfor 4m":
            row_labels.append("VM & Ubuntu 20.04 LTS")
            label = "VM & Ubuntu 20.04 LTS"
        else:
            row_labels.append("MacBookPro & MacOS 10.15.4")
            label = "MacBookPro & MacOS 10.15.4"
        row = []
        x_values = []
        y_values = []
        for percentile, value in results.items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        ax1.plot(x_values, y_values, label=label, color=colors[running_time])
        rows.append(row)
    ax1.set_ylabel("Latency (milliseconds)")
    ax1.set_xlabel("Percentile")
    ax1.set_title("Latency by Percentile Distribution (1th to 100th)")
    ax1.grid()
    # plt.tight_layout()
    plt.legend()

    ax1.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    plot_matrix_sub_plot(ax1, row_labels, rows, col_labels)
    plt.savefig(f"{file_name}_.pdf")
    plt.close(fig)


data_mac = {
    "1%": 0.467,
    "25%": 0.515,
    "50%": 0.539,
    "75%": 0.580,
    "90%": 0.759,
    "99%": 3536.754,
    "99.9%": 5769.656,
    "99.99%": 5991.969,
    "99.999%": 6013.956,
}
data_momentum = {
    "1%": 0.789,
    "25%": 0.804,
    "50%": 0.830,
    "75%": 0.882,
    "90%": 0.941,
    "99%": 1.573,
    "99.9%": 1.664,
    "99.99%": 1.811,
    "99.999%": 4.943,
}

if __name__ == "__main__":
    plot_hdr_histogram(
        {
            "running on\nMacBookPro & MacOS 10.15.4\nfor 4m": data_mac,
            "running on\nVM & Ubuntu 20.04 LTS\nfor 4m": data_momentum,
        },
        "mac_vs_vm_wrk",
    )  # type: ignore
