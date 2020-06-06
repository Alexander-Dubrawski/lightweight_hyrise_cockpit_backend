# type: ignore
from concurrent import futures
from statistics import mean, median, pstdev
from time import time_ns

import numpy as np
from zmq import REQ, Context

from backend.request import Header, Request
from backend.settings import DB_MANAGER_HOST, DB_MANAGER_PORT

CLIENTS = [2, 4]
RUNS = 10


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
    return {"latency": latency, "run_time": (end_benchmark - start_benchmark)}


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
    percentiles = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990]
    percentiles_values = [np.percentile(num, percentile) for percentile in percentiles]
    return {
        number_clinets: {
            "Avg": round(avg_latency / 1_000_000, 3),
            "Median": round(median_latency / 1_000_000, 3),
            "Stdev": round(stdev_latency / 1_000_000, 3),
            "latency distribution": percentiles_values,
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
        results[n_client] = {}
        worker = n_client
        arguments = [RUNS for _ in range(n_client)]
        with futures.ProcessPoolExecutor(worker) as executor:
            res = executor.map(run_clinet, arguments)
        results[n_client] = list(res)
    return results


def main():
    row_results = run_benchmark()
    formatted_results = run_calculations(row_results)
    print(formatted_results)


if __name__ == "__main__":
    main()
