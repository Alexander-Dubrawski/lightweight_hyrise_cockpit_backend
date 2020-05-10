"""CLI used to start the backend API."""
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route("/throughput")
class Throughput(Resource):
    """Return throughput value."""

    def get(self, **kwargs):
        """Return throughput value."""
        return 42
