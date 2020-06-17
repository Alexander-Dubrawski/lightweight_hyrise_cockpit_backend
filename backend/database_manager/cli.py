"""CLI used to start the database manager."""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from backend.settings import (
    BROKER_LISTENING,
    BROKER_PORT,
    DB_MANAGER_LISTENING,
    DB_MANAGER_PORT,
    WORKER_LISTING,
    WORKER_PORT,
    WORKLOAD_PUBSUB_PORT,
    WORKLOAD_SUB_HOST,
)

from .broker import Broker


class Parser:
    """Parse arguments from command line."""

    def __init__(self):
        """Initialize a ArgumentParser."""
        self.parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            "--worker",
            "-w",
            dest="worker",
            metavar="",
            type=int,
            nargs="?",
            help="number workers",
        )
        self.parser.add_argument(
            "--threads",
            "-t",
            dest="threads",
            metavar="",
            type=str,
            nargs="?",
            help="number threads for each worker",
        )

    def get_configuration(self):
        """Return argument configuration."""
        worker = self.parser.parse_args().worker
        threads = self.parser.parse_args().threads
        return {
            "worker": int(worker),
            "threads": int(threads),
        }


def main() -> None:
    """Create and start a database manager."""
    argp = Parser()  # type: ignore
    config = argp.get_configuration()

    try:
        with Broker(
            DB_MANAGER_LISTENING,
            DB_MANAGER_PORT,
            BROKER_LISTENING,
            BROKER_PORT,
            WORKER_LISTING,
            WORKER_PORT,
            WORKLOAD_SUB_HOST,
            WORKLOAD_PUBSUB_PORT,
            mumber_worker=config["worker"],
            number_threads=config["threads"],
        ) as manager_broker:
            print(f"Broker running on port {BROKER_PORT} (Press CTRL+C to quit)")
            manager_broker.run()
    except KeyboardInterrupt:
        print("Broker closed.")


if __name__ == "__main__":
    main()
