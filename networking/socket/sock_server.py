"""Socket based MEC server"""

import socket
import threading
import json
import docker, docker.errors

from utils import send_json, decode_json

class MECServer:
    def __init__(self, host: str="localhost", port: int=3000):
        self.host = host
        self.port = port
        self.docker_client = docker.from_env()
        self.running: bool = False
        self.active_containters = {}
        self.server_socket: socket.socket = None

    def start(self):
        """Start the websocket server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True

        print(f"Server started on {self.host}:{self.port}")

        try:
            while self.running:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                # Start a new thread to handle this client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Server stopped by user")
    
    def handle_client(self, client_socket: socket.socket, addr: tuple[str, int]):
        """Handle individual client connection"""
        client_id = f"{addr[0]}:{addr[1]}"
        try:
            # Receive 4096 bit blocks from client
            data = client_socket.recv(4096)
            if not data:
                print(f"Received empty data from {client_id}")
                return
            try:
                command = decode_json(data)
                print(f"Received command from {client_id}: {str(command)}")

                #TODO Check command format

                # Send ack
                send_json(client_socket, {"status": "starting_service"})

                # Start containter
                container = self.start_container(command["image"], command.get("command"), command.get("environment", {}))

                # Send status update
                send_json(client_socket, {"status":"service_started"})
                # Add to active containers list
                self.active_containters[client_id] = container

            except json.JSONDecodeError as e:
                print(f"Unexpected error parsing JSON from {client_id}: {str(e)}")
                send_json(client_socket, {"error":str(e)})
            except docker.errors.ImageNotFound:
                print(f"Docker image '{command["image"]}' not found")
                send_json(client_socket, {"error":f"Docker image \"{command["image"]}\" not found"})
        except Exception as e:
            print(f"Unexpected error handling client {client_id}: {str(e)}")
    
    def start_container(self, image_name: str, command=None, environment=None):
        """Start a Docker container with given image and other parameters"""
        print(f"Starting container from image: {image_name}")

        container = self.docker_client.containers.run(
            image_name,
            command=command,
            environment=environment,
            detach=True,        # Run container in background
            stdin_open=True,    # Keep STDIN open for input
            tty=True,           # Simulate a terminal interface
            remove=True         # Auto-remove container after it stops
        )

        print(f"Container started: {container.id}")
        return container


if __name__ == "__main__":
    server = MECServer()
    server.start()
