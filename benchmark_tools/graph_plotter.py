from calendar import timegm
from statistics import mean, median
from time import gmtime

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def interpolate(data, steps):
    x_values = []
    y_values = []
    for i in range(0, len(data), steps):
        x_values.append(mean(data[i : i + steps]))
        y_values.append(i)
    return (x_values, y_values)


def plot_line_chart(data, file_name):
    avg_values = []
    med_values = []
    col_labels = []
    figure(num=None, figsize=(12, 6), dpi=80, facecolor="w", edgecolor="k")
    for key, values in data.items():
        values.remove(max(values))
        avg_values.append(f"{round(mean(values) * 1_000, 4)}ms")
        med_values.append(f"{round(median(values) * 1_000, 4)}ms")
        x_values, y_values = interpolate(values, 50)
        plt.plot(y_values, x_values, label=key)
        col_labels.append(key)

    plt.legend(loc="upper left")
    plt.ylabel("time ms")
    plt.xlabel("runs")
    plt.title("Server Processing Latency")
    row_labels = ["AVG", "MED"]
    rows = [avg_values, med_values]
    plt.table(
        cellText=rows,
        rowLabels=row_labels,
        cellLoc="center",
        colLabels=col_labels,
        loc="bottom",
        bbox=[0, -0.29, 1, 0.17],
    )
    plt.subplots_adjust(left=0.2, bottom=0.2)
    ts = timegm(gmtime())
    plt.savefig(f"measurements/{file_name}_{ts}.png")
