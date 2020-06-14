# type: ignore
from calendar import timegm
from concurrent import futures
from json import dumps
from statistics import mean, median, pstdev
from time import gmtime, time_ns

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
from zmq import REQ, Context

from backend.request import Header, Request
from backend.settings import DB_MANAGER_HOST, DB_MANAGER_PORT

CLIENTS = [1, 2, 4, 8, 16, 32, 64]
RUNS = 4096
PERCENTILES = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]


def plot_hdr_histogram(results, file_name):
    fig = figure(num=None, figsize=(40, 30), dpi=300, facecolor="w", edgecolor="k")
    plt.rcParams.update({"font.size": 22})
    col_labels = [f"{percentile}th" for percentile in PERCENTILES]
    rows = []
    row_labels = []
    for number, data in results.items():
        row_labels.append(f"clients: {number}")
        row = []
        y_values = []
        x_values = [str(percentile) for percentile in PERCENTILES]
        for value in data["latency distribution"]:
            y_values.append(value)
            row.append(value)
        rows.append(row)
        plt.plot(
            x_values, y_values, label=f"clients: {number}", linewidth=4.0,
        )
    plt.legend()
    plt.ylabel("Latency (milliseconds)")
    plt.xlabel("Percentile")
    plt.title("Latency by Percentile Distribution")
    plt.grid()
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
    plt.savefig(f"measurements/{file_name}_{ts}.pdf")
    plt.close(fig)


def run_clinet(runs):
    context = Context()
    socket = context.socket(REQ)
    socket.connect(f"tcp://{DB_MANAGER_HOST}:{DB_MANAGER_PORT}")
    latency = []
    start_benchmark = time_ns()
    for _ in range(runs):
        start_ts = time_ns()
        socket.send_json(Request(header=Header(message="get metric"), body={}))
        _ = socket.recv_json()
        end_ts = time_ns()
        latency.append(end_ts - start_ts)
    end_benchmark = time_ns()
    return {
        "latency": latency,
        "run_time": (end_benchmark - start_benchmark),
        "runs": runs,
    }


def claculate_values(args):
    number_clinets, data = args
    complete_latency = []
    complete_runtime = 0
    for element in data:
        complete_latency += element["latency"]
        complete_runtime += element["run_time"] / RUNS
    avg_latency = mean(complete_latency)
    median_latency = median(complete_latency)
    stdev_latency = pstdev(complete_latency)
    num = np.array(complete_latency)
    percentiles_values = [np.percentile(num, percentile) for percentile in PERCENTILES]
    return {
        number_clinets: {
            "Avg": round(avg_latency / 1_000_000, 3),
            "Median": round(median_latency / 1_000_000, 3),
            "Stdev": round(stdev_latency / 1_000_000, 3),
            "latency distribution": [
                round(val / 1_000_000, 3) for val in percentiles_values
            ],
            "throughput": 1 / (complete_runtime / 1_000_000_000),
        }
    }


def run_calculations(data):
    arguments = [(key, value) for key, value in data.items()]
    worker = len(arguments)
    with futures.ProcessPoolExecutor(worker) as executor:
        res = executor.map(claculate_values, arguments)
    results = list(res)
    combined_res = {}
    for result in results:
        combined_res.update(result)
    return combined_res


def run_benchmark():
    results = {}
    for n_client in CLIENTS:
        print(f"running benchmark with {n_client} clients")
        results[n_client] = {}
        worker = n_client
        arguments = [int(RUNS / n_client) for _ in range(n_client)]
        with futures.ProcessPoolExecutor(worker) as executor:
            res = executor.map(run_clinet, arguments)
        results[n_client] = list(res)
    return results


def main():
    row_results = run_benchmark()
    formatted_results = run_calculations(row_results)
    print(formatted_results)
    with open("measurements/zmq_results.txt", "+w") as file:
        file.write(dumps(formatted_results))
    plot_hdr_histogram(formatted_results, "zmq_hdr")


if __name__ == "__main__":
    main()
