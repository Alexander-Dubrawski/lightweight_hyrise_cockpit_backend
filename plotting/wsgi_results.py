# type: ignore
from json import loads


def get_latency_1(number_threads, kind):
    with open(
        f"measurements/wsgi_benchmark_1_ms/formatted_{kind}_results.txt", "r"
    ) as file:
        content = loads(file.read())
    return content[str(number_threads)]["latency_distribution"]


latency_threads_1 = {
    1: get_latency_1(1, "worker"),
    2: get_latency_1(2, "thread"),
    4: get_latency_1(4, "thread"),
    8: get_latency_1(8, "thread"),
    16: get_latency_1(16, "thread"),
    32: get_latency_1(32, "thread"),
    64: get_latency_1(64, "thread"),
}

throughput_threads_1 = {
    1: 7.65,
    2: 9.49,
    4: 8.79,
    8: 8.42,
    16: 8.29,
    32: 8.30,
    64: 8.31,
}

latency_workers_1 = {
    1: get_latency_1(1, "worker"),
    2: get_latency_1(2, "worker"),
    4: get_latency_1(4, "worker"),
    8: get_latency_1(8, "worker"),
    16: get_latency_1(16, "worker"),
    32: get_latency_1(32, "worker"),
    64: get_latency_1(64, "worker"),
}

throughput_workers_1 = {
    1: 7.65,
    2: 13.75,
    4: 27.42,
    8: 54.83,
    16: 100.30,
    32: 192.46,
    64: 154.12,
}


def get_latency_50(number_threads, kind):
    with open(
        f"measurements/wsgi_benchmark_50_ms/formatted_{kind}_results.txt", "r"
    ) as file:
        content = loads(file.read())
    return content[str(number_threads)]["latency_distribution"]


latency_threads_50 = {
    1: {
        "1%": 3315.498,
        "25%": 3317.252,
        "50%": 3318.042,
        "75%": 3318.881,
        "90%": 3319.677,
        "99%": 3321.360,
        "99.9%": 3328.433,
        "99.99%": 3332.435,
    },
    2: get_latency_50(2, "thread"),
    4: get_latency_50(4, "thread"),
    8: get_latency_50(8, "thread"),
    16: get_latency_50(16, "thread"),
    32: get_latency_50(32, "thread"),
    64: get_latency_50(64, "thread"),
}

throughput_threads_50 = {
    1: 0.00,
    2: 0.00,
    4: 1.00,
    8: 1.90,
    16: 4.77,
    32: 8.12,
    64: 8.32,
}

latency_workers_50 = {
    1: {
        "1%": 3315.498,
        "25%": 3317.252,
        "50%": 3318.042,
        "75%": 3318.881,
        "90%": 3319.677,
        "99%": 3321.360,
        "99.9%": 3328.433,
        "99.99%": 3332.435,
    },
    2: get_latency_50(2, "worker"),
    4: get_latency_50(4, "worker"),
    8: get_latency_50(8, "worker"),
    16: get_latency_50(16, "worker"),
    32: get_latency_50(32, "worker"),
    64: get_latency_50(64, "worker"),
}

throughput_workers_50 = {
    1: 0.00,
    2: 0.00,
    4: 1.00,
    8: 1.91,
    16: 4.77,
    32: 9.79,
    64: 19.02,
}


def get_latency_w_t(number_t_w):
    with open(
        "measurements/wsgi_benchmark_50_ms/formatted_worker_thread_results.txt", "r"
    ) as file:
        content = loads(file.read())
    percentiles = content[str(number_t_w)]["latency_percentiles"]["percentiles"]
    return {
        "1%": percentiles[0],
        "10%": percentiles[9],
        "20%": percentiles[19],
        "30%": percentiles[29],
        "40%": percentiles[39],
        "50%": percentiles[49],
        "60%": percentiles[59],
        "70%": percentiles[69],
        "80%": percentiles[79],
        "90%": percentiles[89],
        "99%": percentiles[98],
        "99.9%": content[str(number_t_w)]["latency_distribution"]["99.9%"],
        "99.99%": content[str(number_t_w)]["latency_distribution"]["99.99%"],
    }


latency_threads_worker = {
    (1, 1): get_latency_w_t((1, 1)),
    (80, 1): get_latency_w_t((80, 1)),
    (2, 32): get_latency_w_t((2, 32)),
    (3, 32): get_latency_w_t((3, 32)),
    (4, 32): get_latency_w_t((4, 32)),
    (3, 16): get_latency_w_t((3, 16)),
    (4, 16): get_latency_w_t((4, 16)),
    (2, 64): get_latency_w_t((2, 64)),
}

throughput_threads_worker = {
    (1, 1): 0.00,
    (80, 1): 12.20,
    (2, 32): 12.80,
    (3, 32): 17.49,
    (4, 32): 19.18,
    (3, 16): 14.49,
    (4, 16): 18.67,
    (2, 64): 12.65,
}
