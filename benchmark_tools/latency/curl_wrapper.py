"""Wrapper for curl execution."""
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
CURL_FORMAT_FILE = "./benchmark_tools/latency/curl-format.txt"


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
