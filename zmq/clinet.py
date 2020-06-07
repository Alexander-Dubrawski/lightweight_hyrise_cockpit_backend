import zmq

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

#  Do 10 requests, waiting each time for a response

print("Send json")
data = {"action": "intern"}
socket.send_json(data)
response = socket.recv_json()
print(f"Response from server:\n{response}")
data = {"action": "worker"}
socket.send_json(data)
response = socket.recv_json()
print(f"Response from worker:\n{response}")
