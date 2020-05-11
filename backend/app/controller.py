"""CLI used to start the backend API."""
from typing import List

from flask import Flask, request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_cors import CORS
from flask_restx import Api, Resource

from .interface import DatabaseInterface, DetailedDatabaseInterface, WorkloadInterface
from .model import DetailedDatabase, Workload
from .schema import DatabaseSchema, DetailedDatabaseSchema, WorkloadSchema
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
