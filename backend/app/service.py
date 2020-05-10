"""Service for back-end api."""

from .interface import WorkloadInterface
from .model import Workload


class WorkloadService:
    """Services of the Workload Controller."""

    @classmethod
    def get_workload(cls) -> Workload:
        """Get all Workloads.
        Returns a list of all Workloads.
        """
        return Workload(workload_name="tpch", frequency=200)

    @classmethod
    def create(cls, interface: WorkloadInterface) -> Workload:
        """Create a Workload.
        Returns the created Workload.
        Returns None if a Workload with the given ID already exists.
        """
        return Workload(**interface)
