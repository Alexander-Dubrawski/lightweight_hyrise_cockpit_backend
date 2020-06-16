from calendar import timegm
from datetime import datetime
from json import dumps, loads
from os import mkdir
from subprocess import check_output, run
from time import gmtime, sleep

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

NUMBER_CLIENTS = 64
quantity = [1, 2, 4, 8, 16, 32, 64]
worker_threads = [(64, 1), (2, 2), (2, 64), (4, 2), (4, 64), (8, 64), (8, 2)]
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/flask_metric"
DURATION_IN_MINUTES = 10
WSGI_INIT_TIME = 60


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def format_results(results):
    """Extract Requests/sec and Latency from wrk output and saves it in a dictionary structure."""
    formatted_results = {}
    for number_t_p, output in results.items():
        split_output = output.splitlines()
        index_latency_values = split_output.index("latency_values:")
        index_request_values = split_output.index("request_values:")
        index_latency_distribution = split_output.index("latency_distribution:")
        index_percentiles = split_output.index("percentiles:")
        formatted_results[number_t_p] = {
            "Latency": loads(split_output[index_latency_values + 1]),
            "latency_distribution": loads(split_output[index_latency_distribution + 1]),
            "Req/Sec": loads(split_output[index_request_values + 1]),
            "latency_percentiles": loads(split_output[index_percentiles + 1]),
        }
    return formatted_results


def start_wsgi_server_worker(number_worker):
    run(
        [
            "numactl",
            "-m",
            "0",
            "--physcpubind",
            "0-19",
            "pipenv",
            "run",
            "gunicorn",
            "--daemon",
            "--capture-output",
            "--error-logfil",
            "gunicorn_w_error.txt",
            "--log-file",
            "gunicorn_w_log.txt",
            "-w",
            str(number_worker),
            "--threads",
            "1",
            "--backlog",
            "80",
            "backend.app.controller:app",
        ]
    )
    sleep(WSGI_INIT_TIME)


def start_wsgi_server_threads(number_threads):
    run(
        [
            "numactl",
            "-m",
            "0",
            "--physcpubind",
            "0-19",
            "pipenv",
            "run",
            "gunicorn",
            "--daemon",
            "--capture-output",
            "--error-logfil",
            "gunicorn_t_error.txt",
            "--log-file",
            "gunicorn_t_log.txt",
            "--worker-class=gthread",
            "-w",
            "1",
            "--threads",
            str(number_threads),
            "--backlog",
            "80",
            "backend.app.controller:app",
        ]
    )
    sleep(WSGI_INIT_TIME)


def start_wsgi_server_threads_and_worker(number_threads, number_worker):
    run(
        [
            "numactl",
            "-m",
            "0",
            "--physcpubind",
            "0-19",
            "pipenv",
            "run",
            "gunicorn",
            "--daemon",
            "--capture-output",
            "--error-logfil",
            "gunicorn_t_w_error.txt",
            "--log-file",
            "gunicorn_t_w_log.txt",
            "--worker-class=gthread",
            "-w",
            str(number_worker),
            "--threads",
            str(number_threads),
            "--backlog",
            "80",
            "backend.app.controller:app",
        ]
    )
    sleep(WSGI_INIT_TIME)


def execute_wrk_on_endpoint():
    """Background process to execute wrk."""
    return check_output(
        f"numactl -m 0 --physcpubind 20-79 wrk -t{NUMBER_CLIENTS} -c{NUMBER_CLIENTS} -s ./benchmark_tools/report.lua -d{DURATION_IN_MINUTES}m --timeout 20s {BACKEND_URL}",
        shell=True,
    ).decode("utf-8")


def run_benchmark_on_threaded_wsgi(path):
    """Run wrk sequential on all endpoints."""
    results = {}
    for number_threads in quantity:
        print(f"Run for {number_threads} threads")
        start_wsgi_server_threads(number_threads)
        results[number_threads] = execute_wrk_on_endpoint()
        with open(f"{path}/threaded_results.txt", "a+") as file:
            file.write(f"\n{number_threads} threads\n")
            file.write(results[number_threads])
        run(["fuser", "-k", f"{BACKEND_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def run_benchmark_on_worker_wsgi(path):
    """Run wrk sequential on all endpoints."""
    results = {}
    for number_worker in quantity:
        print(f"Run for {number_worker} workers")
        start_wsgi_server_worker(number_worker)
        results[number_worker] = execute_wrk_on_endpoint()
        with open(f"{path}/worker_results.txt", "a+") as file:
            file.write(f"\n{number_worker} workers\n")
            file.write(results[number_worker])
        run(["fuser", "-k", f"{BACKEND_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def run_benchmark_on_worker_thread_wsgi(path):
    """Run wrk sequential on all endpoints."""
    results = {}
    for number_worker_thread in worker_threads:
        print(
            f"Run for {number_worker_thread[0]} workers and {number_worker_thread[1]} threads"
        )
        start_wsgi_server_threads_and_worker(
            number_threads=number_worker_thread[1],
            number_worker=number_worker_thread[0],
        )
        results[number_worker_thread] = execute_wrk_on_endpoint()
        with open(f"{path}/worker_thread_results.txt", "a+") as file:
            file.write(
                f"\n{number_worker_thread[0]} workers and {number_worker_thread[1]} threads\n"
            )
            file.write(results[number_worker_thread])
        run(["fuser", "-k", f"{BACKEND_PORT}/tcp"])
        sleep(WSGI_INIT_TIME)
    return results


def run_bnechmark():
    path = create_folder("wsgi_benchmark")
    results = {}
    results["threads"] = run_benchmark_on_threaded_wsgi(path)
    results["worker"] = run_benchmark_on_worker_wsgi(path)
    results["thread_worker"] = run_benchmark_on_worker_thread_wsgi(path)
    formatted_results = {}
    formatted_results["threads"] = format_results(results["threads"])
    formatted_results["worker"] = format_results(results["worker"])
    formatted_results["thread_worker"] = format_results(results["thread_worker"])
    formatted_results["thread_worker"] = {
        str(k): v for k, v in formatted_results["thread_worker"].items()
    }

    with open(f"{path}/formatted_thread_results.txt", "+w") as file:
        file.write(dumps(formatted_results["threads"]))
    with open(f"{path}/formatted_worker_results.txt", "+w") as file:
        file.write(dumps(formatted_results["worker"]))
    with open(f"{path}/formatted_worker_thread_results.txt", "+w") as file:
        file.write(dumps(formatted_results["thread_worker"]))


if __name__ == "__main__":
    run_bnechmark()  # type: ignore
