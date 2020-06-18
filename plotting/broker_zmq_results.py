# type: ignore
from json import loads


def get_latency(number, io_length, kind):
    percentiles = [1, 25, 50, 75, 90, 99, 99.9, 99.99]
    with open(
        f"measurements/long_zmq_{io_length}/formatted_results_{kind}.txt", "r"
    ) as file:
        content = loads(file.read())
    results = {}
    count = 0
    for per in percentiles:
        results[f"{per}%"] = content[str(number)]["latency distribution"][count]
        count += 1
    return results


def get_throughput(number, io_length, kind):
    with open(
        f"measurements/long_zmq_{io_length}/formatted_results_{kind}.txt", "r"
    ) as file:
        content = loads(file.read())
    return content[str(number)]["throughput"]


latency_threads_1 = {
    1: get_latency((1, 1), 1, "worker_threads"),
    2: get_latency(2, 1, "thread"),
    4: get_latency(4, 1, "thread"),
    8: get_latency(8, 1, "thread"),
    16: get_latency(16, 1, "thread"),
    32: get_latency(32, 1, "thread"),
    64: get_latency(64, 1, "thread"),
    128: get_latency(128, 1, "thread"),
}

throughput_threads_1 = {
    1: get_throughput((1, 1), 1, "worker_threads"),
    2: get_throughput(2, 1, "thread"),
    4: get_throughput(4, 1, "thread"),
    8: get_throughput(8, 1, "thread"),
    16: get_throughput(16, 1, "thread"),
    32: get_throughput(32, 1, "thread"),
    64: get_throughput(64, 1, "thread"),
    128: get_throughput(128, 1, "thread"),
}

latency_workers_1 = {
    1: get_latency((1, 1), 1, "worker_threads"),
    2: get_latency(2, 1, "worker"),
    4: get_latency(4, 1, "worker"),
    8: get_latency(8, 1, "worker"),
    16: get_latency(16, 1, "worker"),
    32: get_latency(32, 1, "worker"),
    64: get_latency(64, 1, "worker"),
    128: get_latency(128, 1, "worker"),
}

throughput_workers_1 = {
    1: get_throughput((1, 1), 1, "worker_threads"),
    2: get_throughput(2, 1, "worker"),
    4: get_throughput(4, 1, "worker"),
    8: get_throughput(8, 1, "worker"),
    16: get_throughput(16, 1, "worker"),
    32: get_throughput(32, 1, "worker"),
    64: get_throughput(64, 1, "worker"),
    128: get_throughput(128, 1, "worker"),
}


latency_threads_worker_1 = {
    (2, 32): get_latency((2, 32), 1, "worker_threads"),
    (3, 32): get_latency((3, 32), 1, "worker_threads"),
    (4, 16): get_latency((4, 16), 1, "worker_threads"),
    (3, 16): get_latency((3, 16), 1, "worker_threads"),
    (2, 64): get_latency((2, 64), 1, "worker_threads"),
}

throughput_threads_worker_1 = {
    (2, 32): get_throughput((2, 32), 1, "worker_threads"),
    (3, 32): get_throughput((3, 32), 1, "worker_threads"),
    (4, 16): get_throughput((4, 16), 1, "worker_threads"),
    (3, 16): get_throughput((3, 16), 1, "worker_threads"),
    (2, 64): get_throughput((2, 64), 1, "worker_threads"),
}

latency_threads_50 = {
    1: get_latency((1, 1), 50, "worker_threads"),
    2: get_latency(2, 50, "thread"),
    4: get_latency(4, 50, "thread"),
    8: get_latency(8, 50, "thread"),
    16: get_latency(16, 50, "thread"),
    32: get_latency(32, 50, "thread"),
    64: get_latency(64, 50, "thread"),
    128: get_latency(128, 50, "thread"),
}

throughput_threads_50 = {
    1: get_throughput((1, 1), 50, "worker_threads"),
    2: get_throughput(2, 50, "thread"),
    4: get_throughput(4, 50, "thread"),
    8: get_throughput(8, 50, "thread"),
    16: get_throughput(16, 50, "thread"),
    32: get_throughput(32, 50, "thread"),
    64: get_throughput(64, 50, "thread"),
    128: get_throughput(128, 50, "thread"),
}

latency_workers_50 = {
    1: get_latency((1, 1), 50, "worker_threads"),
    2: get_latency(2, 50, "worker"),
    4: get_latency(4, 50, "worker"),
    8: get_latency(8, 50, "worker"),
    16: get_latency(16, 50, "worker"),
    32: get_latency(32, 50, "worker"),
    64: get_latency(64, 50, "worker"),
    128: get_latency(128, 50, "worker"),
}

throughput_workers_50 = {
    1: get_throughput((1, 1), 50, "worker_threads"),
    2: get_throughput(2, 50, "worker"),
    4: get_throughput(4, 50, "worker"),
    8: get_throughput(8, 50, "worker"),
    16: get_throughput(16, 50, "worker"),
    32: get_throughput(32, 50, "worker"),
    64: get_throughput(64, 50, "worker"),
    128: get_throughput(128, 50, "worker"),
}

latency_threads_worker_50 = {
    (2, 32): get_latency((2, 32), 50, "worker_threads"),
    (3, 32): get_latency((3, 32), 50, "worker_threads"),
    (4, 16): get_latency((4, 16), 50, "worker_threads"),
    (3, 16): get_latency((3, 16), 50, "worker_threads"),
    (2, 64): get_latency((2, 64), 50, "worker_threads"),
}

throughput_threads_worker_50 = {
    (2, 32): get_throughput((2, 32), 50, "worker_threads"),
    (3, 32): get_throughput((3, 32), 50, "worker_threads"),
    (4, 16): get_throughput((4, 16), 50, "worker_threads"),
    (3, 16): get_throughput((3, 16), 50, "worker_threads"),
    (2, 64): get_throughput((2, 64), 50, "worker_threads"),
}


def get_contentt(io_length, kind):
    with open(f"measurements/formatted_{io_length}_{kind}_results.txt", "r") as file:
        content = loads(file.read())
    return content


detailed_thread_latency_1 = get_contentt(1, "threads")
detailed_thread_latency_50 = get_contentt(50, "threads")
detailed_worker_latency_1 = get_contentt(1, "worker")
detailed_worker_latency_50 = get_contentt(50, "worker")
detailed_worker_thread_latency_1 = get_contentt(50, "worker_thread")
detailed_worker_thread_latency_50 = get_contentt(50, "worker_thread")
