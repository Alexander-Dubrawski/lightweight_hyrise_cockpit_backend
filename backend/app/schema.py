"""Schema for back-end api."""

from marshmallow import Schema
from marshmallow.fields import Integer, String


class WorkloadSchema(Schema):
    """Schema of a Workload."""

    workload_name = String(description="Name of the workload.", required=True,)
    frequency = Integer(
        description="Number of queries generated per second.", required=True
    )
