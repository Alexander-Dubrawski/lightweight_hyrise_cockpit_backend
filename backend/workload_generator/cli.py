"""CLI used to start the workload generator."""
from backend.settings import (
    GENERATOR_LISTENING,
    GENERATOR_PORT,
    WORKLOAD_LISTENING,
    WORKLOAD_PUBSUB_PORT,
)

from .generator import WorkloadGenerator


def main() -> None:
    """Create and start a workload generator."""
    try:
        with WorkloadGenerator(
            GENERATOR_LISTENING,
            GENERATOR_PORT,
            WORKLOAD_LISTENING,
            WORKLOAD_PUBSUB_PORT,
        ) as workload_generator:
            print(
                f"Workload generator running on port {GENERATOR_PORT} (Press CTRL+C to quit)"
            )
            workload_generator.start()
    except KeyboardInterrupt:
        print("Workload Generator closed.")


if __name__ == "__main__":
    main()
