import json
import socket

def send_json(socket: socket.socket, data: dict):
    """Send JSON data over a socket."""
    socket.sendall(json.dumps(data).encode("utf-8"))

def decode_json(data: str):
    return json.loads(data.decode("utf-8"))