from calendar import timegm
from concurrent import futures
from datetime import datetime
from json import dumps
from os import mkdir
from statistics import mean, median, pstdev
from subprocess import Popen, run
from time import gmtime, sleep, time_ns

import numpy as np
from zmq import REQ, Context

from backend.request import Header, Request
from backend.settings import BROKER_LISTENING, BROKER_PORT

quantity = [2, 4, 8, 16, 32, 64, 128]
worker_threads = [
    (1, 1),
    (2, 32),
    (3, 32),
    (4, 16),
    (3, 16),
    (4, 16),
    (2, 64),
]
RUNS = 100_000
NUMBER_CLIENTS = 64
PERCENTILES = [1, 25, 50, 75, 90, 99, 99.9, 99.99]
WSGI_INIT_TIME = 60


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def start_manager(number_workers, number_threads):
    sub_process = Popen(
        [
            "numactl",
            "-m",
            "0",
            "--physcpubind",
            "0-19",
            "pipenv",
            "run",
            "python",
            "-m",
            "backend.database_manager.cli",
            "-w",
            str(number_workers),
            "-t",
            str(number_threads),
        ]
    )
    sleep(WSGI_INIT_TIME)
    return sub_process


def run_clinet(runs):
    context = Context()
    socket = context.socket(REQ)
    socket.connect(f"tcp://{BROKER_LISTENING}:{BROKER_PORT}")
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


def run_benchmark_threads(path):
    results = {}
    for n_thread in quantity:
        print(f"running benchmark with {n_thread} threads")
        _ = start_manager(number_workers=1, number_threads=n_thread)
        results[n_thread] = {}
        worker = NUMBER_CLIENTS
        arguments = [int(RUNS / NUMBER_CLIENTS) for _ in range(NUMBER_CLIENTS)]
        with futures.ProcessPoolExecutor(worker) as executor:
            res = executor.map(run_clinet, arguments)
        results[n_thread] = list(res)
        with open(f"{path}/{n_thread}_threads_results.txt", "+w") as file:
            file.write(dumps(results[n_thread]))
        with open(f"{path}/{n_thread}_threads_results_formatted.txt", "+w") as file:
            file.write(dumps(claculate_values((64, results[n_thread]))))
        run(["fuser", "-k", f"{BROKER_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def run_benchmark_worker(path):
    results = {}
    for n_worker in quantity:
        print(f"running benchmark with {n_worker} worker")
        _ = start_manager(number_workers=n_worker, number_threads=1)
        results[n_worker] = {}
        worker = NUMBER_CLIENTS
        arguments = [int(RUNS / NUMBER_CLIENTS) for _ in range(NUMBER_CLIENTS)]
        with futures.ProcessPoolExecutor(worker) as executor:
            res = executor.map(run_clinet, arguments)
        results[n_worker] = list(res)
        with open(f"{path}/{n_worker}_worker_results.txt", "+w") as file:
            file.write(dumps(results[n_worker]))
        with open(f"{path}/{n_worker}_worker_results_formatted.txt", "+w") as file:
            file.write(dumps(claculate_values((64, results[n_worker]))))
        run(["fuser", "-k", f"{BROKER_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def run_benchmark_worker_threads(path):
    results = {}
    for n_worker, n_thread in worker_threads:
        print(f"running benchmark with {n_worker} worker and {n_thread}")
        _ = start_manager(number_workers=n_worker, number_threads=n_thread)
        results[(n_worker, n_thread)] = {}
        worker = NUMBER_CLIENTS
        arguments = [int(RUNS / NUMBER_CLIENTS) for _ in range(NUMBER_CLIENTS)]
        with futures.ProcessPoolExecutor(worker) as executor:
            res = executor.map(run_clinet, arguments)
        results[(n_worker, n_thread)] = list(res)
        with open(
            f"{path}/{n_worker}_worker_{n_thread}_threads_results.txt", "+w"
        ) as file:
            file.write(dumps(results[(n_worker, n_thread)]))
        with open(
            f"{path}/{n_worker}_worker_{n_thread}_threads_results_formatted.txt", "+w"
        ) as file:
            file.write(dumps(claculate_values((64, results[(n_worker, n_thread)]))))
        run(["fuser", "-k", f"{BROKER_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def main():
    path = create_folder("long_zmq_50")
    row_results_threads = run_benchmark_threads(path)
    row_results_worker = run_benchmark_worker(path)
    row_results_worker_threads = run_benchmark_worker_threads(path)
    formatted_results_thread = run_calculations(row_results_threads)
    formatted_results_worker = run_calculations(row_results_worker)
    formatted_results_worker_threads = run_calculations(row_results_worker_threads)
    with open(f"{path}/formatted_results_thread.txt", "+w") as file:
        file.write(dumps(formatted_results_thread))
    with open(f"{path}/formatted_results_worker.txt", "+w") as file:
        file.write(dumps(formatted_results_worker))
    formatted_results_worker_threads = {
        str(k): v for k, v in formatted_results_worker_threads.items()
    }
    with open(f"{path}/formatted_results_worker_threads.txt", "+w") as file:
        file.write(dumps(formatted_results_worker_threads))


if __name__ == "__main__":
    main()  # type: ignore
