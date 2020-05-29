import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def plot_hdr_histogram(data, file_name):
    colors = {
        "running for 10s": "cornflowerblue",
        "running for 30s": "darkcyan",
        "running for 1m": "indianred",
        "running for 2m": "sandybrown",
        "running for 4m": "purple",
        "running for 8m": "aqua",
        "running for 16m": "magenta",
        "mac running for 16m": "blue",
        "vm running for 16m": "orange",
    }
    fig = figure(num=None, figsize=(30, 10), dpi=80, facecolor="w", edgecolor="k")
    for running_time, results in data.items():
        x_values = []
        y_values = []
        for percentile, value in results.items():
            x_values.append(percentile)
            y_values.append(value)
        plt.plot(
            x_values, y_values, label=f"{running_time}", color=colors[running_time]
        )
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0)
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    plt.title("Latency by Percentile Distribution")
    plt.grid()
    plt.savefig(f"{file_name}_.pdf")
    plt.close(fig)


sequential_data = {
    "running for 10s": {
        "1%": 0.470,
        "25%": 0.515,
        "50%": 0.544,
        "75%": 0.569,
        "90%": 0.605,
        "99%": 0.881,
        "99.9%": 2.949,
        "99.99%": 5.042,
        "99.999%": 5.042,
    },
    "running for 30s": {
        "1%": 0.456,
        "25%": 0.504,
        "50%": 0.526,
        "75%": 0.555,
        "90%": 0.589,
        "99%": 0.815,
        "99.9%": 2.281,
        "99.99%": 5.023,
        "99.999%": 6.316,
    },
    "running for 1m": {
        "1%": 0.453,
        "25%": 0.503,
        "50%": 0.530,
        "75%": 0.559,
        "90%": 0.593,
        "99%": 0.817,
        "99.9%": 2.509,
        "99.99%": 5.012,
        "99.999%": 6.609,
    },
    "running for 2m": {
        "1%": 0.449,
        "25%": 0.500,
        "50%": 0.524,
        "75%": 0.555,
        "90%": 0.590,
        "99%": 0.844,
        "99.9%": 2.449,
        "99.99%": 4.897,
        "99.999%": 5.881,
    },
    "running for 4m": {
        "1%": 0.458,
        "25%": 0.506,
        "50%": 0.526,
        "75%": 0.553,
        "90%": 0.585,
        "99%": 0.807,
        "99.9%": 2.133,
        "99.99%": 5.762,
        "99.999%": 6.454,
    },
    "running for 8m": {
        "1%": 0.451,
        "25%": 0.500,
        "50%": 0.527,
        "75%": 0.560,
        "90%": 0.600,
        "99%": 0.852,
        "99.9%": 2.162,
        "99.99%": 4.488,
        "99.999%": 7.287,
    },
    "running for 16m": {
        "1%": 0.470,
        "25%": 0.514,
        "50%": 0.534,
        "75%": 0.562,
        "90%": 0.594,
        "99%": 0.836,
        "99.9%": 2.018,
        "99.99%": 5.026,
        "99.999%": 5.191,
    },
}

parallel_data = {
    "running for 10s": {
        "1%": 0.513,
        "25%": 1.523,
        "50%": 1.621,
        "75%": 1.671,
        "90%": 1.739,
        "99%": 2.444,
        "99.9%": 5.997,
        "99.99%": 8.664,
        "99.999%": 9.313,
    },
    "running for 30s": {
        "1%": 0.502,
        "25%": 0.586,
        "50%": 0.696,
        "75%": 0.836,
        "90%": 0.997,
        "99%": 2.021,
        "99.9%": 4.808,
        "99.99%": 7.532,
        "99.999%": 7.578,
    },
    "running for 1m": {
        "1%": 0.521,
        "25%": 0.786,
        "50%": 1.475,
        "75%": 1.658,
        "90%": 1.768,
        "99%": 2.085,
        "99.9%": 3.631,
        "99.99%": 8.340,
        "99.999%": 8.561,
    },
    "running for 2m": {
        "1%": 0.519,
        "25%": 0.750,
        "50%": 1.438,
        "75%": 1.603,
        "90%": 1.664,
        "99%": 1.941,
        "99.9%": 4.005,
        "99.99%": 7.156,
        "99.999%": 7.774,
    },
    "running for 4m": {
        "1%": 0.514,
        "25%": 0.703,
        "50%": 1.416,
        "75%": 1.600,
        "90%": 1.674,
        "99%": 2.007,
        "99.9%": 3.615,
        "99.99%": 7.622,
        "99.999%": 8.665,
    },
    "running for 8m": {
        "1%": 0.515,
        "25%": 0.709,
        "50%": 1.408,
        "75%": 1.625,
        "90%": 1.698,
        "99%": 1.959,
        "99.9%": 3.640,
        "99.99%": 7.971,
        "99.999%": 8.011,
    },
    "running for 16m": {
        "1%": 0.514,
        "25%": 0.725,
        "50%": 1.468,
        "75%": 1.608,
        "90%": 1.687,
        "99%": 2.135,
        "99.9%": 4.059,
        "99.99%": 7.089,
        "99.999%": 7.382,
    },
}

data_mac_system_noise = {
    "running for 16m": {
        "1%": 0.470,
        "25%": 0.521,
        "50%": 0.548,
        "75%": 0.588,
        "90%": 0.777,
        "99%": 109.902,
        "99.9%": 1319.000,
        "99.99%": 1770.862,
        "99.999%": 1858.774,
    }
}

if __name__ == "__main__":
    plot_hdr_histogram(sequential_data, "sequential_wrk")  # type: ignore
    plot_hdr_histogram(parallel_data, "parallel_wrk")  # type: ignore
    plot_hdr_histogram(data_mac_system_noise, "mac_sequential_wrk")  # type: ignore
    plot_hdr_histogram({"mac running for 16m": data_mac_system_noise["running for 16m"], "vm running for 16m": sequential_data["running for 16m"]}, "mac_vs_vm_wrk")  # type: ignore
