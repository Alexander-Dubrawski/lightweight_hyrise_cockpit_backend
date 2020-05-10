"""Interface for back-end api."""

from typing import TypedDict


class WorkloadInterface(TypedDict):
    """Interface of a Workload."""

    workload_name: str
    frequency: int
