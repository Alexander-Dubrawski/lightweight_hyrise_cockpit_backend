# type: ignore
# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>
import json
import threading
import time

import zmq

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5555")
backend.bind("tcp://*:5560")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)


def worker_routine():
    """Worker routine"""
    context = zmq.Context()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5570")

    while True:
        _ = socket.recv_json()
        reply = {"reply": "from worker"}
        socket.send_json(reply)


def main():
    # Prepare our context and sockets
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    workers = context.socket(zmq.DEALER)
    frontend.bind("tcp://*:5556")
    workers.bind("tcp://*:5570")

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(workers, zmq.POLLIN)
    thread = threading.Thread(target=worker_routine)
    thread.start()
    time.sleep(1)

    while True:
        socks = dict(poller.poll())

        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv_multipart()
            identity, delimeter_fram, data = message
            formatted_data = json.loads(data.decode("utf-8"))
            if formatted_data["action"] == "worker":
                workers.send_multipart(message)
            else:
                reply = {"reply": "from server"}
                json_string = json.dumps(reply)
                frontend.send_multipart(
                    [identity, delimeter_fram, json_string.encode()]
                )

        if socks.get(workers) == zmq.POLLIN:
            message = workers.recv_multipart()
            frontend.send_multipart(message)


if __name__ == "__main__":
    main()
