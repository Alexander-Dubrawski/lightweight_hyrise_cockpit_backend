"""CLI used to start the database manager."""
from backend.settings import (
    DB_MANAGER_LISTENING,
    DB_MANAGER_PORT,
    WORKER_PORT,
    WORKLOAD_PUBSUB_PORT,
    WORKLOAD_SUB_HOST,
)

from .manager import DatabaseManager


def main() -> None:
    """Create and start a database manager."""
    try:
        with DatabaseManager(
            DB_MANAGER_LISTENING,
            DB_MANAGER_PORT,
            WORKLOAD_SUB_HOST,
            WORKLOAD_PUBSUB_PORT,
            WORKER_PORT,
        ) as database_manager:
            print(
                f"Database manager running on port {DB_MANAGER_PORT} (Press CTRL+C to quit)"
            )
            database_manager.start()
    except KeyboardInterrupt:
        print("Database Manager closed.")


if __name__ == "__main__":
    main()
