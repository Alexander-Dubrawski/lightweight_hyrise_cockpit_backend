# type: ignore
# flake8: noqa
import time
from multiprocessing import Process

import zmq

NUMBER_WORKER = 1


def worker_task():
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5009")
    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        broker, empty, client, empty, request = socket.recv_multipart()
        socket.send_multipart([broker, b"", client, b"", b"OK"])


def worker_p(broker_id):
    context = zmq.Context.instance()
    broker = context.socket(zmq.ROUTER)
    broker.setsockopt(zmq.IDENTITY, b"WORKER")
    broker.connect("tcp://127.0.0.1:5007")
    print("Connected with broker")
    backend = context.socket(zmq.ROUTER)
    backend.bind("tcp://127.0.0.1:5009")
    print("bind backend")

    worker_processes = []
    for _ in range(NUMBER_WORKER):
        process = Process(target=worker_task)
        process.start()

    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    workers = []

    print(broker_id)
    broker.send_multipart([broker_id, b"", b"READY"])
    print(f"broker send ready")
    poller.register(broker, zmq.POLLIN)
    print(f"broker {broker}")
    print(f"backend {backend}")
    # message = broker.recv_multipart()
    # print(f"broker got message from broker -> {message}")
    # broker.send_multipart([broker_id, b"", b"READY"])

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            # we need to unpack the last three values. This is the inner envelop
            worker, empty, broker_data = request[:3]
            if not workers:
                # Poll for clients now that a worker is available
                # poller.register(broker, zmq.POLLIN)
                print("broker in poll")
            workers.append(worker)
            if broker_data != b"READY" and len(request) > 3:
                # If client reply, send rest back to broker
                worker, empty, broker_data, empty, client, empty, data = request
                print(f"Send to router {[broker_data, client, data]}")
                broker.send_multipart([broker_data, b"", client, b"", data])

        if broker in sockets:
            print("Inside B Poll")
            # Get next client request, route to last-used worker
            message = broker.recv_multipart()
            print(f"worker process res message -> {message}")
            roker, empty, client, empty, request = message
            print(f"Worker Process res Broker -> {message}")
            worker = workers.pop(0)
            if worker:
                broker.send(b"READY")
            backend.send_multipart([worker, b"", broker_id, b"", client, b"", request])


def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://127.0.0.1:5555")
    backend = context.socket(zmq.ROUTER)
    backend.setsockopt(zmq.IDENTITY, b"BROKER")
    backend.bind("tcp://127.0.0.1:5007")

    worker_processes = []
    for _ in range(NUMBER_WORKER):
        process = Process(target=worker_p, args=(b"BROKER",))
        process.start()

    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    workers = []

    # request = backend.recv_multipart()
    # backend.send_multipart([b"WORKER", b"", b"Hallo"])
    # request = backend.recv_multipart()
    # import pdb; pdb.set_trace()

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            # import pdb; pdb.set_trace()
            print(f"Broker res backend-> {request}")
            # we need to unpack the last three values. This is the inner envelop
            worker, empty, client = request[:3]
            if not workers:
                # Poll for clients now that a worker is available
                poller.register(frontend, zmq.POLLIN)
            workers.append(worker)
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                empty, reply = request[3:]
                frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            message = frontend.recv_multipart()
            client, empty, request = message
            print(f"Broker res frontend-> {message}")
            worker = workers.pop(0)
            backend.send_multipart([worker, b"", client, b"", request])
            print(f"semd {[worker, client, request]}")
            if not workers:
                # Don't poll clients if no workers are available
                poller.unregister(frontend)

    # Clean up
    backend.close()
    frontend.close()
    context.term()


if __name__ == "__main__":
    main()
