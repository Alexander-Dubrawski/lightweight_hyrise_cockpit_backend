# type: ignore
from json import loads


def read_json(number_db):
    with open(f"measurements/{number_db}_formatted_system_results.txt", "r") as file:
        content = loads(file.read())
    return content


def get_latency(number_db):
    with open("measurements/formatted_user_results.txt", "r") as file:
        content = loads(file.read())
    return content[str(number_db)]["manager_metric"]["latency_percentiles"][
        "percentiles"
    ]


latency_percentiles = {
    1: get_latency(1),
    10: get_latency(10),
    20: get_latency(20),
    40: get_latency(40),
}

throughput = {
    1: 18.12,
    10: 18.52,
    20: 18.35,
    40: 15.92,
}

latency = {
    1: {
        "1%": 54.006,
        "50%": 55.133,
        "60%": latency_percentiles[1][59],
        "70%": latency_percentiles[1][69],
        "80%": latency_percentiles[1][79],
        "90%": latency_percentiles[1][89],
        "99%": 55.737,
        "99.9%": 56.515,
        "99.99%": 732.576,
    },
    10: {
        "1%": 53.215,
        "50%": 53.801,
        "60%": latency_percentiles[10][59],
        "70%": latency_percentiles[10][69],
        "80%": latency_percentiles[10][79],
        "90%": latency_percentiles[10][89],
        "99%": 56.446,
        "99.9%": 69.067,
        "99.99%": 762.082,
    },
    20: {
        "1%": 52.763,
        "50%": 53.222,
        "60%": latency_percentiles[20][59],
        "70%": latency_percentiles[20][69],
        "80%": latency_percentiles[20][79],
        "90%": latency_percentiles[20][89],
        "99%": 73.113,
        "99.9%": 87.099,
        "99.99%": 741.987,
    },
    40: {
        "1%": 53.780,
        "50%": 56.699,
        "60%": latency_percentiles[40][59],
        "70%": latency_percentiles[40][69],
        "80%": latency_percentiles[40][79],
        "90%": latency_percentiles[40][89],
        "99%": 115.537,
        "99.9%": 158.488,
        "99.99%": 766.132,
    },
}

cpu_usage = {
    1: read_json(1),
    10: read_json(10),
    20: read_json(20),
    40: read_json(40),
}
