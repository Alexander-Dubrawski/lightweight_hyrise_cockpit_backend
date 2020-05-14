"""Tool for executing curl on endpoint."""
from statistics import mean, median
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

RUNS = 100
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
CURL_FORMAT_FILE = "./benchmark_tools/curl-format.txt"

GET_ENDPOINTS = [
    "workload",
    "database",
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def create_latency_intervals(timestamps):
    """Creates a dictionary for all times values."""
    time_values = {
        "namelookup": float(timestamps[0]),
        "connect": float(timestamps[1]),
        "appconnect": float(timestamps[2]),
        "pretransfer": float(timestamps[3]),
        "redirect": float(timestamps[4]),
        "starttransfer": float(timestamps[5]),
        "total": float(timestamps[6]),
    }
    return time_values


def add_database(database_id):
    """Add database."""
    url = f"{BACKEND_URL}/database"
    header_accept = "accept: application/json"
    header_content_type = "Content-Type: application/json"
    data = f'{{ \\"port\\": \\"string\\", \\"id\\": \\"{database_id}\\", \\"number_workers\\": 8, \\"host\\": \\"string\\"}}'
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}" -H "{header_content_type}" -d "{data}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def delete_database(database_id):
    """Delete database."""
    url = f"{BACKEND_URL}/database"
    header_accept = "accept: application/json"
    header_content_type = "Content-Type: application/json"
    data = f'{{ \\"id\\": \\"{database_id}\\"}}'
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X DELETE "{url}" -H "{header_accept}" -H "{header_content_type}" -d "{data}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def start_worker():
    """Start worker."""
    url = f"{BACKEND_URL}/worker"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def stop_worker():
    """Stop worker."""
    url = f"{BACKEND_URL}/worker"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X DELETE "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def start_workload():
    """Start workload."""
    url = f"{BACKEND_URL}/workload"
    header_accept = "accept: application/json"
    header_content_type = "Content-Type: application/json"
    data = '{ \\"frequency\\": 1000, \\"workload_name\\": \\"some_workload\\"}'
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}" -H "{header_content_type}" -d "{data}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def stop_workload():
    """Stop workload."""
    url = f"{BACKEND_URL}/workload"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X DELETE "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def post_sql(database_id):
    """Execute sql request."""
    url = f"{BACKEND_URL}/sql"
    header_accept = "accept: application/json"
    header_content_type = "Content-Type: application/json"
    data = f'{{ \\"query\\": \\"some_query\\", \\"id\\": \\"{database_id}\\"}}'
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}" -H "{header_content_type}" -d "{data}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def execute_get(endpoint):
    """Execute endpoint."""
    url = f"{BACKEND_URL}/{endpoint}"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s "{url}"', shell=True
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def get_endpoint_benchmark():
    for enpoint in GET_ENDPOINTS:
        print(f"Run on {enpoint}")
        server_process_times = []
        for _ in range(RUNS):
            results = execute_get(enpoint)
            server_process_times.append(results["total"] - results["pretransfer"])
        print(f"Avg: {mean(server_process_times) * 1_000}ms")
        print(f"Median: {median(server_process_times) * 1_000}ms")


def add_delete_database():
    add_server_process_times = []
    delete_server_process_times = []
    for _ in range(RUNS):
        add_result = add_database("db")
        add_server_process_times.append(add_result["total"] - add_result["pretransfer"])
        delete_result = delete_database("db")
        delete_server_process_times.append(
            delete_result["total"] - delete_result["pretransfer"]
        )

    print("Run add database")
    print(f"Avg: {mean(add_server_process_times) * 1_000}ms")
    print(f"Median: {median(add_server_process_times) * 1_000}ms")

    print("Run delete database")
    print(f"Avg: {mean(delete_server_process_times) * 1_000}ms")
    print(f"Median: {median(delete_server_process_times) * 1_000}ms")


def start_stop_worker():
    add_database("db")
    start_server_process_times = []
    stop_server_process_times = []
    for _ in range(RUNS):
        start_result = start_worker()
        start_server_process_times.append(
            start_result["total"] - start_result["pretransfer"]
        )
        stop_result = stop_worker()
        stop_server_process_times.append(
            stop_result["total"] - stop_result["pretransfer"]
        )
    delete_database("db")

    print("Run start worker")
    print(f"Avg: {mean(start_server_process_times) * 1_000}ms")
    print(f"Median: {median(start_server_process_times) * 1_000}ms")

    print("Run stop worker")
    print(f"Avg: {mean(stop_server_process_times) * 1_000}ms")
    print(f"Median: {median(stop_server_process_times) * 1_000}ms")


def start_stop_workload():
    start_server_process_times = []
    stop_server_process_times = []
    for _ in range(RUNS):
        start_result = start_workload()
        start_server_process_times.append(
            start_result["total"] - start_result["pretransfer"]
        )
        stop_result = stop_workload()
        stop_server_process_times.append(
            stop_result["total"] - stop_result["pretransfer"]
        )

    print("Run start workload")
    print(f"Avg: {mean(start_server_process_times) * 1_000}ms")
    print(f"Median: {median(start_server_process_times) * 1_000}ms")

    print("Run stop workload")
    print(f"Avg: {mean(stop_server_process_times) * 1_000}ms")
    print(f"Median: {median(stop_server_process_times) * 1_000}ms")


def execute_sql():
    add_database("db")
    server_process_times = []
    for _ in range(RUNS):
        result = post_sql("db")
        server_process_times.append(result["total"] - result["pretransfer"])
    print("Run execute sql")
    print(f"Avg: {mean(server_process_times) * 1_000}ms")
    print(f"Median: {median(server_process_times) * 1_000}ms")

    delete_database("db")


def run_benchmark():
    """Run benchmark."""
    get_endpoint_benchmark()
    add_delete_database()
    start_stop_worker()
    start_stop_workload()
    execute_sql()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
