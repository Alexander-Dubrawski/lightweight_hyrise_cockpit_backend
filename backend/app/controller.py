"""CLI used to start the backend API."""
from flask import Flask, request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_cors import CORS
from flask_restx import Api, Resource

from .interface import WorkloadInterface
from .model import Workload
from .schema import WorkloadSchema
from .service import WorkloadService

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
