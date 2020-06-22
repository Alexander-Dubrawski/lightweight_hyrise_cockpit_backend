# type: ignore
from json import loads


def get_latency(number, io_length, broker_type, kind):
    percentiles = [1, 25, 50, 75, 90, 99, 99.9, 99.99]
    with open(
        f"measurements/long_zmq_{broker_type}_{io_length}/formatted_results_{kind}.txt",
        "r",
    ) as file:
        content = loads(file.read())
    results = {}
    count = 0
    for per in percentiles:
        results[f"{per}%"] = content[str(number)]["latency distribution"][count]
        count += 1
    return results


def get_throughput(number, io_length, broker_type, kind):
    with open(
        f"measurements/long_zmq_{broker_type}_{io_length}/formatted_results_{kind}.txt",
        "r",
    ) as file:
        content = loads(file.read())
    return content[str(number)]["throughput"]


def get_formatted_latency(io_length, broker_type, kind):
    keys = [2, 4, 8, 16, 32, 64, 128]
    results = {}
    for key in keys:
        results[key] = (get_latency(key, io_length, broker_type, kind),)
    results[1] = (get_latency((1, 1), io_length, broker_type, "worker_threads"),)
    return results


def get_formatted_throughput(io_length, broker_type, kind):
    keys = [2, 4, 8, 16, 32, 64, 128]
    results = {}
    for key in keys:
        results[key] = (get_throughput(key, io_length, broker_type, kind),)
    results[1] = (get_throughput((1, 1), io_length, broker_type, "worker_threads"),)
    return results


latency_threads_balanced_1 = get_formatted_latency(1, "balanced", "thread")
throughput_threads_balanced_1 = get_formatted_throughput(1, "balanced", "thread")
latency_workers_balanced_1 = get_formatted_latency(1, "balanced", "worker")
throughput_workers_balanced_1 = get_formatted_throughput(1, "balanced", "worker")

latency_threads_not_balanced_1 = get_formatted_latency(1, "not_balanced", "thread")
throughput_threads_not_balanced_1 = get_formatted_throughput(
    1, "not_balanced", "thread"
)
latency_workers_not_balanced_1 = get_formatted_latency(1, "not_balanced", "worker")
throughput_workers_not_balanced_1 = get_formatted_throughput(
    1, "not_balanced", "worker"
)

latency_threads_balanced_50 = get_formatted_latency(50, "balanced", "thread")
throughput_threads_balanced_50 = get_formatted_throughput(50, "balanced", "thread")
latency_workers_balanced_50 = get_formatted_latency(50, "balanced", "worker")
throughput_workers_balanced_50 = get_formatted_throughput(50, "balanced", "worker")

latency_threads_not_balanced_50 = get_formatted_latency(50, "not_balanced", "thread")
throughput_threads_not_balanced_50 = get_formatted_throughput(
    50, "not_balanced", "thread"
)
latency_workers_not_balanced_50 = get_formatted_latency(50, "not_balanced", "worker")
throughput_workers_not_balanced_50 = get_formatted_throughput(
    50, "not_balanced", "worker"
)


def get_throughput_slow_worker(number, io_length, broker_type, kind):
    with open(
        f"measurements/slow_worker_long_zmq_{broker_type}_{io_length}/formatted_results_{kind}.txt",
        "r",
    ) as file:
        content = loads(file.read())
    return content[str(number)]["throughput"]


def get_latency_slow_worker(number, io_length, broker_type, kind):
    percentiles = [1, 25, 50, 75, 90, 99, 99.9, 99.99, 99.999]
    with open(
        f"measurements/slow_worker_long_zmq_{broker_type}_{io_length}/formatted_results_{kind}.txt",
        "r",
    ) as file:
        content = loads(file.read())
    results = {}
    count = 0
    for per in percentiles:
        results[f"{per}%"] = content[str(number)]["latency distribution"][count]
        count += 1
    return results


def get_formatted_latency_slow_worker(io_length, broker_type, kind):
    keys = [16, 32, 64]
    results = {}
    for key in keys:
        results[key] = (get_latency_slow_worker(key, io_length, broker_type, kind),)
    return results


def get_formatted_throughput_slow_worker(io_length, broker_type, kind):
    keys = [16, 32, 64]
    results = {}
    for key in keys:
        results[key] = (get_throughput_slow_worker(key, io_length, broker_type, kind),)
    return results


latency_workers_balanced_slow = get_formatted_latency_slow_worker(
    1, "balanced", "worker"
)
throughput_workers_balanced_slow = get_formatted_throughput_slow_worker(
    1, "balanced", "worker"
)

latency_workers_not_balanced_slow = get_formatted_latency_slow_worker(
    1, "not_balanced", "worker"
)
throughput_workers_not_balanced_slow = get_formatted_throughput_slow_worker(
    1, "not_balanced", "worker"
)
