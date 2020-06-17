"""CLI used to start the database manager."""
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

NUMBER_WORKER = 1
NUMBER_THREAD = 1


def main() -> None:
    """Create and start a database manager."""
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
            NUMBER_WORKER,
            NUMBER_THREAD,
        ) as manager_broker:
            print(f"Broker running on port {BROKER_PORT} (Press CTRL+C to quit)")
            manager_broker.run()
    except KeyboardInterrupt:
        print("Broker closed.")


if __name__ == "__main__":
    main()
