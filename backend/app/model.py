"""Model for back-end api."""


class Workload:
    """Model of a Workload."""

    def __init__(self, workload_name: str, frequency: int):
        """Initialize a Workload model."""
        self.workload_name: str = workload_name
        self.frequency: int = frequency
