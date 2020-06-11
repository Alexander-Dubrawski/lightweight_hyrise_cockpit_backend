# type: ignore
from statistics import mean, median, pstdev
from time import time_ns

import numpy as np
from zmq import REQ, Context

from backend.settings import DB_MANAGER_HOST, DB_MANAGER_PORT

PERCENTILES = [1, 25, 50, 75.000, 90, 99.000, 99.900, 99.990, 99.999]
RUNS = 10_000


def run_client(runs):

    latency = []
    start_benchmark = time_ns()
    for _ in range(runs):
        start_ts = time_ns()
        context = Context()
        socket = context.socket(REQ)
        socket.connect(f"tcp://{DB_MANAGER_HOST}:{DB_MANAGER_PORT}")
        socket.close()
        context.term()
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
    percentiles_values = [np.percentile(num, percentile) for percentile in PERCENTILES]
    return {
        number_clinets: {
            "Avg": round(avg_latency / 1_000_000, 3),
            "Median": round(median_latency / 1_000_000, 3),
            "Stdev": round(stdev_latency / 1_000_000, 3),
            "latency distribution": [
                round(val / 1_000_000, 3) for val in percentiles_values
            ],
        }
    }


if __name__ == "__main__":
    res = run_client(RUNS)
    f_res = claculate_values((1, [res]))
    print(f_res)
