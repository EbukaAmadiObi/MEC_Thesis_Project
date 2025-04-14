"""Socket based MEC server"""

import socket
import threading
import json
import docker, docker.errors
from docker.models.containers import Container

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
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable address reuse
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
            print("\nServer stopped by user")

            # Close server socket
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
            self.running = False
    
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
                send_json(client_socket, {
                    "status":"service_started",
                    "container_id": container.id,
                    "name": container.name
                    })
                # Add to active containers list
                self.active_containters[client_id] = container

                self.start_stream(container, client_socket)

            except json.JSONDecodeError as e:
                print(f"Unexpected error parsing JSON from {client_id}: {str(e)}")
                send_json(client_socket, {"error":str(e)})
            except docker.errors.ImageNotFound:
                print(f"Docker image '{command["image"]}' not found")
                send_json(client_socket, {"error":f"Docker image \"{command["image"]}\" not found"})
        except Exception as e:
            print(f"Unexpected error handling client {client_id}: {str(e)}")
            send_json(client_socket, {"error":f"{str(e)}"})
    
    def start_container(self, image_name: str, command=None, environment=None) -> Container:
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

        print(f"Container started: {container.name}")
        return container
    
    def start_stream(self, container: Container, client_socket: socket.socket):
        """Start bidirectional stream, connecting container and client"""
        print(f"Starting stream for container: {container.name}")

        # Get container streams with proper configuration
        container_socket = self.docker_client.api.attach_socket(
            container.id, 
            params={
                'stdin': 1,
                'stdout': 1,
                'stderr': 1,
                'stream': 1,
                'logs': 1
            }
        )

        # Create threads for streaming both ways
        client_to_container = threading.Thread(
            target=self.client_to_container_stream,
            args=(client_socket, container_socket, container.name)
        )
        client_to_container.daemon = True

        container_to_client = threading.Thread(
            target=self.container_to_client_stream,
            args=(client_socket, container_socket, container.name)
        )
        container_to_client.daemon = True

        client_to_container.start()
        container_to_client.start()

        # Wait for threads to complete (container exit or client disconnect)
        container_to_client.join()
        client_to_container.join()

        print("Deleting threads...")
        del container_to_client
        del client_to_container
        print("Deleted!")
    
    def client_to_container_stream(self, client_socket: socket.socket, container_socket, container_name):
        """Stream data from client to container"""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    print(f"Client disconnected from container {container_name}")
                    break
                
                # Send data to container
                try:
                    container_socket._sock.sendall(data)
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Container {container_name} stream closed")
                    break
                
                # Check if container is still running
                try:
                    container = self.docker_client.containers.get(container_name)
                    if container.status != "running":
                        print(f"Container {container_name} is no longer running (status: {container.status})")
                        break
                except docker.errors.NotFound:
                    print(f"Container {container_name} no longer exists")
                    break
        except Exception as e:
            print(f"Error streaming to container {container_name}: {str(e)}")
        finally:
            print(f"Stopped streaming from client to container {container_name}")
        
    def container_to_client_stream(self, client_socket, container_socket, container_name):
        try:
            while True:
                data = container_socket.read(4096)  # read data from container
                if not data:
                    print(f"Container {container_name} stream closed")
                    break
            
                # Send data to client
                try:
                    client_socket.sendall(data)
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Client disconnected while streaming from container {container_name}")
                    break
                
                # Check if container is still running
                try:
                    container = self.docker_client.containers.get(container_name)
                    if container.status != "running":
                        print(f"Container {container_name} is no longer running (status: {container.status})")
                        break
                except docker.errors.NotFound:
                    print(f"Container {container_name} no longer exists")
                    break
        except Exception as e:
            print(f"Error streaming from container {container_name}: {str(e)}")
        finally:
            print(f"Stopped streaming from container {container_name} to client")

if __name__ == "__main__":
    server = MECServer()
    server.start()
