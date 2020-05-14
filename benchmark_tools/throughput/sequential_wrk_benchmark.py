"""Tool for executing wrk benchmark."""

from subprocess import run  # nosec

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_SECOUNDS = 10
ENDPOINTS = ["worklaod", "database", "queue_length", "storage", "throughput", "latency"]


def wrk_background_process(url):
    """Background process to execute wrk."""
    sub_process = run(  # nosec
        ["wrk", "-t1", "-c1", f"-d{DURATION_IN_SECOUNDS}s", f"{url}"],
        capture_output=True,
    )
    print(sub_process.stdout.decode("utf-8"))
    print(sub_process.stderr.decode("utf-8"))


def run_benchmark():
    """Run wrk benchmark on endpoints."""
    for endpoint in ENDPOINTS:
        wrk_background_process(f"{BACKEND_URL}/{endpoint}")


if __name__ == "__main__":
    run_benchmark()  # type: ignore
