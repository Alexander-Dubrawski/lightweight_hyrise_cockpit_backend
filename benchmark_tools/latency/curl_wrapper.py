"""Wrapper for curl execution."""
from subprocess import check_output

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
CURL_FORMAT_FILE = "./benchmark_tools/latency/curl-format.txt"


def create_latency_intervals(timestamps):
    """
    Creates a dictionary for all times values.

    The time values are defined as follows:
        namelookup: The time it took from the start until the name resolving was completed.
        connect: The time it took from the start until the connect to the remote host (or proxy) was completed.
        appconnect: The time it took from the start until the SSL connect/handshake with the remote host was completed.
        pretransfer: The time it took from the start until the file transfer is just about to begin.
        redirect: The time it took for all redirection steps include name lookup, connect,
                pretransfer and transfer before final transaction was started.
                So, this is zero if no redirection took place.
        starttransfer: The time it took from the start until the first byte is received by libcurl.
        total: Total time of the previous request.

    source: https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
    """
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
    """
    Add database.

    Send POST request via curl.
    """
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
    """
    Delete database.

    Send DELETE request via curl.
    """
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
    """
    Start worker.

    Send POST request via curl.
    """
    url = f"{BACKEND_URL}/worker"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def stop_worker():
    """
    Stop worker.

    Send DELETE request via curl.
    """
    url = f"{BACKEND_URL}/worker"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X DELETE "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def start_workload():
    """
    Start workload.

    Send POST request via curl.
    """
    url = f"{BACKEND_URL}/workload"
    header_accept = "accept: application/json"
    header_content_type = "Content-Type: application/json"
    data = '{ \\"frequency\\": 10000, \\"workload_name\\": \\"some_workload\\"}'
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X POST "{url}" -H "{header_accept}" -H "{header_content_type}" -d "{data}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def stop_workload():
    """
    Stop workload.

    Send DELETE request via curl.
    """
    url = f"{BACKEND_URL}/workload"
    header_accept = "accept: application/json"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s -X DELETE "{url}" -H "{header_accept}"',
        shell=True,
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)


def post_sql(database_id):
    """
    Execute sql request.

    Send POST request via curl.
    """
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
    """
    Execute endpoint.

    Send GET request to endpoint via curl.
    """
    url = f"{BACKEND_URL}/{endpoint}"
    output = check_output(
        f'curl -w "@{CURL_FORMAT_FILE}" -o /dev/null -s "{url}"', shell=True
    )
    output = output.decode("utf-8").split()
    return create_latency_intervals(output)
