# type: ignore
from concurrent import futures
from time import sleep, time_ns


def execute_code(runs):
    for i in range(runs):
        print(i)
        sleep(0.001)


def execute_benchmark(total_runs, workers):
    arguments = [total_runs / workers for _ in range(workers)]
    start_ts = time_ns()
    with futures.ThreadPoolExecutor(workers) as executor:
        _ = executor.map(execute_code, arguments)
    end_ts = time_ns()
    print(f"Execution time for {workers} threads: {(end_ts-start_ts) / 1000000}ms")


def main():
    runs = 100
    threads = [1]
    for thread in threads:
        execute_benchmark(runs, thread)


if __name__ == "__main__":
    main()
