"""Schema for back-end api."""

from marshmallow import Schema, post_load
from marshmallow.fields import Dict, Integer, List, String

from .model import Database, DetailedDatabase, SqlQuery, SqlResponse


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


class SqlQuerySchema(Schema):
    """Schema of a SQL query."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    query = String(
        title="SQL query",
        description="Sql query to execute on database.",
        required=True,
        example="SELECT 1;",
    )

    @post_load
    def make_sql_query(self, data, **kwargs):
        """Return SqlQuery object."""
        return SqlQuery(**data)


class SqlResponseSchema(Schema):
    """Schema of a SQL response."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    results = List(
        List(String()),
        title="Results",
        description="Results from query execution.",
        required=True,
        example=[["1", "100", "first"], ["2", "None", "second"], ["3", "42", "third"]],
    )

    @post_load
    def make_sql_query(self, data, **kwargs):
        """Return SqlResponse object."""
        return SqlResponse(**data)


class StorageSchema(Schema):
    """Schema of a storage response."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    results = Dict(
        title="Storage information", description="Storage usage.", required=True,
    )


class ThroughputSchema(Schema):
    """Schema of a throughput response."""

    id = String(
        title="Database ID",
        description="Used to identify a database.",
        required=True,
        example="hyrise-1",
    )
    throughput = Integer(
        title="Throughput information",
        description="Throughput of the last second.",
        required=True,
        example=200,
    )
