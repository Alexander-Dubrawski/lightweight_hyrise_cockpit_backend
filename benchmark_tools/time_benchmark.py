from .wrk_benchmark import run_wrk_parallel


def run_benchmark():
    run_wrk_parallel()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
