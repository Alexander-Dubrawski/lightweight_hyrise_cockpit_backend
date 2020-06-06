# type: ignore
from concurrent import futures
from statistics import mean, median, pstdev
from time import time_ns

import numpy as np
from zmq import REQ, Context

from backend.request import Header, Request
from backend.settings import DB_MANAGER_HOST, DB_MANAGER_PORT

CLIENTS = 2
RUNS = 1000


def run_clinet(args):
    runs, ipc_message = args
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


def main():
    worker = CLIENTS
    arguments = [(RUNS, b"Hello") for _ in range(CLIENTS)]
    with futures.ProcessPoolExecutor(worker) as executor:
        res = executor.map(run_clinet, arguments)
    results = list(res)
    complete_latency = []
    complete_runtime = 0
    for element in results:
        complete_latency += element["latency"]
        complete_runtime += element["run_time"] / RUNS
    complete_runtime = complete_runtime / CLIENTS
    avg_latency = mean(complete_latency)
    median_latency = median(complete_latency)
    stdev_latency = pstdev(complete_latency)
    num = np.array(complete_latency)
    percentiles = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990]
    percentiles_values = [np.percentile(num, percentile) for percentile in percentiles]

    print(f"Latency Avg {round(avg_latency / 1_000_000, 3)}ms")
    print(f"Latency Med {round(median_latency / 1_000_000, 3)}ms")
    print(f"Latency Med {round(stdev_latency / 1_000_000, 3)}ms")
    print("\nLatency distribution:")
    for percentile, value in zip(percentiles, percentiles_values):
        print(f"{percentile}th:  {round(value / 1_000_000, 3)}ms")


if __name__ == "__main__":
    main()
