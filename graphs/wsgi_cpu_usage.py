# type: ignore
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from wsgi_cpu_usage_results import combi, only_worker


def plot():
    fig = figure(num=None, figsize=(20, 10), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    plt.plot(
        only_worker["time_stamp"],
        only_worker["usage"],
        label="80 processes",
        color="blue",
        linewidth=4.0,
    )
    plt.plot(
        combi["time_stamp"],
        combi["usage"],
        label="4 processes with 16 threads",
        color="orange",
        linewidth=4.0,
    )
    plt.legend()
    plt.ylabel("CPU usage (%)")
    plt.xlabel("time in sec")
    plt.title("CPU usage of workers")
    plt.tight_layout()
    plt.savefig("worker_cpu.pdf")
    plt.close(fig)


if __name__ == "__main__":
    plot()
