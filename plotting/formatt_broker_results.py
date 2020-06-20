# type: ignore
from json import dumps, loads

import numpy as np


def claculate_latency_distribution(data):
    percentiles = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99, 99.999]
    complete_latency = []
    for element in data:
        complete_latency += element["latency"]
    num = np.array(complete_latency)
    percentiles_values = {}
    for percentile in percentiles:
        val = np.percentile(num, percentile)
        percentiles_values[f"{percentile}%"] = round(val / 1_000_000, 3)
    return percentiles_values


def get_latency_distribution(io_length, kind):
    quantity = [2, 4, 8, 16, 32, 64, 128]
    results = {}
    for quan in quantity:
        with open(
            f"measurements/long_zmq_{io_length}/{quan}_{kind}_results.txt", "r"
        ) as file:
            content = loads(file.read())
        results[quan] = claculate_latency_distribution(content)
    with open(
        f"measurements/long_zmq_{io_length}/1_worker_1_threads_results.txt", "r"
    ) as file:
        content = loads(file.read())
    results[1] = claculate_latency_distribution(content)

    with open(f"measurements/formatted_{io_length}_{kind}_results.txt", "+w") as file:
        file.write(dumps(results))


def get_latency_distribution_combi(io_length):
    quantities = [
        (2, 32),
        (3, 32),
        (4, 16),
        (3, 16),
        (2, 64),
    ]
    results = {}
    for quan in quantities:
        with open(
            f"measurements/long_zmq_{io_length}/{quan[0]}_worker_{quan[1]}_threads_results.txt",
            "r",
        ) as file:
            content = loads(file.read())
        results[quan] = claculate_latency_distribution(content)
    results = {str(k): v for k, v in results.items()}
    with open(
        f"measurements/formatted_{io_length}_worker_thread_results.txt", "+w"
    ) as file:
        file.write(dumps(results))


def main():
    get_latency_distribution(1, "worker")
    get_latency_distribution(1, "threads")
    get_latency_distribution(50, "worker")
    get_latency_distribution(50, "threads")
    get_latency_distribution_combi(1)
    get_latency_distribution_combi(50)


if __name__ == "__main__":
    main()
