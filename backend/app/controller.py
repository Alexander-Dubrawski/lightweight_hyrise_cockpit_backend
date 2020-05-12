"""CLI used to start the backend API."""
from typing import Dict, List, Optional, Union

from flask import Flask, request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_cors import CORS
from flask_restx import Api, Resource

from .interface import (
    DatabaseInterface,
    DetailedDatabaseInterface,
    SqlQueryInterface,
    WorkloadInterface,
)
from .model import DetailedDatabase, QueueLength, SqlResponse, Status, Workload
from .schema import (
    DatabaseSchema,
    DetailedDatabaseSchema,
    LatencySchema,
    QueueLengthSchema,
    SqlQuerySchema,
    SqlResponseSchema,
    StatusSchema,
    StorageSchema,
    ThroughputSchema,
    WorkloadSchema,
)
from .service import DatabaseService, WorkloadService

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route("/workload")
class WorkloadController(Resource):
    """Controller of Workloads."""

    @responds(schema=WorkloadSchema, api=api)
    def get(self) -> Workload:
        """Get all Workloads."""
        return WorkloadService.get_workload()

    @accepts(schema=WorkloadSchema, api=api)
    @responds(schema=WorkloadSchema, api=api)
    def post(self) -> Response:
        """Create a Workload."""
        interface: WorkloadInterface = request.parsed_obj
        return Response(status=WorkloadService.create(interface))

    def delete(self) -> Response:
        """Delete a Workload."""
        return Response(status=WorkloadService.delete())


@api.route("/database")
class DatabasesController(Resource):
    """Controller for access and register databases."""

    @responds(schema=DetailedDatabaseSchema(many=True), api=api)
    def get(self) -> List[DetailedDatabase]:
        """Get all databases."""
        return DatabaseService.get_databases()

    @accepts(schema=DetailedDatabaseSchema, api=api)
    def post(self) -> Response:
        """Register new database."""
        interface: DetailedDatabaseInterface = DetailedDatabaseInterface(
            id=request.parsed_obj.id,
            host=request.parsed_obj.host,
            port=request.parsed_obj.port,
            number_workers=request.parsed_obj.number_workers,
        )
        status_code = DatabaseService.register_database(interface)
        return Response(status=status_code)

    @accepts(schema=DatabaseSchema, api=api)
    def delete(self) -> Response:
        """De-register database."""
        interface: DatabaseInterface = DatabaseInterface(id=request.parsed_obj.id)
        status_code = DatabaseService.deregister_database(interface)
        return Response(status=status_code)


@api.route("/worker")
class WorkerController(Resource):
    """Manage start and stop of worker pool at all databases."""

    def post(self) -> Response:
        """Start worker pool for all databases."""
        status_code = DatabaseService.start_worker_pool()
        return Response(status=status_code)

    def delete(self) -> Response:
        """Start worker pool for all databases."""
        status_code = DatabaseService.close_worker_pool()
        return Response(status=status_code)


@api.route("/status")
class StatusController(Resource):
    """Manage status of all databases."""

    @responds(schema=StatusSchema(many=True), api=api)
    def get(self) -> List[Status]:
        """Return status for all databases."""
        return DatabaseService.get_status()


@api.route("/sql")
class SqlController(Resource):
    """Execute SQL query on database."""

    @api.response(404, "Database not found.")
    @accepts(schema=SqlQuerySchema, api=api)
    @responds(schema=SqlResponseSchema, api=api)
    def post(self) -> Union[Optional[Response], SqlResponse]:
        """Execute SQL query."""
        interface: SqlQueryInterface = SqlQueryInterface(
            id=request.parsed_obj.id, query=request.parsed_obj.query
        )
        response, status_code = DatabaseService.execute_sql(interface)
        if status_code == 200:
            return response
        return Response(status=status_code)


@api.route("/storage")
class StorgaeController(Resource):
    """Return storage information of database."""

    @responds(schema=StorageSchema(many=True), api=api)
    def get(self) -> List[Dict]:
        """Return storage information for all databases."""
        return DatabaseService.get_storage()


@api.route("/throughput")
class ThroughputController(Resource):
    """Return throughput information of database."""

    @responds(schema=ThroughputSchema(many=True), api=api)
    def get(self) -> List[Dict]:
        """Return throughput information for all databases."""
        return DatabaseService.get_throughput()


@api.route("/latency")
class LatencyController(Resource):
    """Return throughput information of database."""

    @responds(schema=LatencySchema(many=True), api=api)
    def get(self) -> List[Dict]:
        """Return throughput information for all databases."""
        return DatabaseService.get_latency()


@api.route("/queue_length")
class QueueLengthController(Resource):
    """Return Queue length of database."""

    @responds(schema=QueueLengthSchema(many=True), api=api)
    def get(self) -> List[QueueLength]:
        """Return throughput information for all databases."""
        return DatabaseService.get_queue_length()
