import matplotlib.pyplot as plt
from matplotlib import ticker

colors = {
    "running for 10s": "cornflowerblue",
    "running for 30s": "darkcyan",
    "running for 1m": "indianred",
    "running for 2m": "sandybrown",
    "running for 4m": "purple",
    "running for 8m": "aqua",
    "running for 16m": "magenta",
    "running on\nVM & Ubuntu 20.04 LTS\nfor 4m": "blue",
    "running on\nMacBookPro & MacOS 10.15.4\nfor 4m": "orange",
}


def plot_hdr_histogram(data, file_name):
    # fig = figure(num=None, figsize=(34, 12), dpi=300, facecolor="w", edgecolor="k")
    # ax1 = fig.add_subplot(221, label="100th")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 20))
    # make a little extra space between the subplots
    col_labels = list(data["running on\nVM & Ubuntu 20.04 LTS\nfor 4m"].keys())
    rows = []
    row_labels = []
    for running_time, results in data.items():
        if running_time == "running on\nVM & Ubuntu 20.04 LTS\nfor 4m":
            row_labels.append("VM & Ubuntu 20.04 LTS")
        else:
            row_labels.append("MacBookPro & MacOS 10.15.4")
        row = []
        x_values = []
        y_values = []
        for percentile, value in results.items():
            x_values.append(percentile)
            y_values.append(value)
            row.append(value)
        ax1.plot(
            x_values, y_values, label=f"{running_time}", color=colors[running_time]
        )
        rows.append(row)
    # ax1.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0)
    ax1.set_ylabel("Latency (milliseconds)")
    ax1.set_xlabel("Percentile")
    ax1.set_title("Latency by Percentile Distribution (1th to 100th)")
    ax1.grid()
    ax1.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0)
    fig.subplots_adjust(hspace=0.4)
    percentiles = ["1%", "25%", "50%", "75%", "90%"]
    for running_time, results in data.items():
        x_values = []
        y_values = []
        for percentile in percentiles:
            x_values.append(percentile)
            y_values.append(results[percentile])
        ax2.plot(
            x_values, y_values, label=f"{running_time}", color=colors[running_time]
        )
    ax2.set_ylabel("Latency (milliseconds)")
    ax2.set_xlabel("Percentile")
    ax2.set_title("Latency by Percentile Distribution (1th to 90th)")
    ax2.grid()
    ax2.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0)
    ax2.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, top=0.8)
    ax1.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax2.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
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
    "100%": 6016.399,
}
data_momentum = {
    "1%": 0.513,
    "25%": 0.532,
    "50%": 0.550,
    "75%": 0.571,
    "90%": 0.609,
    "99%": 0.813,
    "99.9%": 1.363,
    "99.99%": 5.680,
    "99.999%": 9.526,
    "100%": 10.208,
}

if __name__ == "__main__":
    plot_hdr_histogram(
        {
            "running on\nMacBookPro & MacOS 10.15.4\nfor 4m": data_mac,
            "running on\nVM & Ubuntu 20.04 LTS\nfor 4m": data_momentum,
        },
        "mac_vs_vm_wrk",
    )  # type: ignore
