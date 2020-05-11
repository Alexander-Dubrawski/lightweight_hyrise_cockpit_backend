"""Schema for back-end api."""

from marshmallow import Schema, post_load
from marshmallow.fields import Integer, String

from .model import Database, DetailedDatabase


class WorkloadSchema(Schema):
    """Schema of a Workload."""

    workload_name = String(description="Name of the workload.", required=True,)
    frequency = Integer(
        description="Number of queries generated per second.", required=True
    )


class DatabaseSchema(Schema):
    """Schema of a Database."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )

    @post_load
    def make_database(self, data, **kwargs):
        """Return database object."""
        return Database(**data)


class DetailedDatabaseSchema(Schema):
    """Schema of a detailed Database."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    host = String(
        title="Host",
        description="Host to log in to.",
        required=True,
        example="vm.example.com",
    )
    port = String(
        title="Port",
        description="Port of the host to log in to.",
        required=True,
        example="1234",
    )
    number_workers = Integer(
        title="Number of initial database worker processes.",
        description="",
        required=True,
        example=8,
    )

    @post_load
    def make_detailed_database(self, data, **kwargs):
        """Return detailed database object."""
        return DetailedDatabase(**data)


class StatusSchema(Schema):
    """Schema of a status."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    worker_pool_status = String(
        title="Worker pool status",
        description="Status of worker pool",
        required=True,
        example="running",
    )
