"""CLI used to start the backend API."""
from backend.settings import BACKEND_LISTENING, BACKEND_PORT

from .controller import app


def main() -> None:
    """Create and start a backend API."""
    app.run(host=BACKEND_LISTENING, port=BACKEND_PORT, debug=False, threaded=True)


if __name__ == "__main__":
    main()
