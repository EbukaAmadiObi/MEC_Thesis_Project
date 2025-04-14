"""Socket based MEC client"""

import socket
import json

from utils import send_json, decode_json

class MECClient:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        self.running = False
        self.container_id = None
        self.server_socket = None
    
    def connect(self) -> bool:
        """Connect to the MEC server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running at {self.host}:{self.port}?")
            return False
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False
    
    def start_service(self, image_name: str, command: str=None, environment: str=None) -> bool:
        """Send command to start service on server"""

        command_req = {
            "action": "start_service",
            "image": image_name
            }
        if command:
            command_req["command"] = command
        if environment:
            command_req["environment"] = environment
        
        try:
            send_json(self.server_socket, command_req)
            print(f"Sent \"start service\" command for \"{image_name}\"")

            response = self.receive_json()
            if "error" in response:
                print(f"Error in starting service: {response["error"]}")
                return False
            elif response.get("status") == "starting_service":
                print(f"Server is starting service...")

            response = self.receive_json()
            if "error" in response:
                print(f"Error in starting service: {response["error"]}")
                return False
            elif response.get("status") == "service_started":
                print(f"Service started successfully with container name {response["name"]}")
                return True
            
            print(f"Unexpected response: {response}")
            return False

        except Exception as e:
            print(f"Exception occurred while sending start command: {str(e)}")
            return False
    
    def send(self, dict: dict):
        send_json(self.server_socket, dict)

    def receive_json(self) -> dict[str, str]:     # TODO: add timeout
        data = b""
        """Receive and parse JSON response from server"""
        while True:
            chunk = self.server_socket.recv(4096)
            if not chunk:
                print("Connection closed by server")
                return None
            data += chunk
            try:
                return decode_json(data)
            except json.JSONDecodeError:
                continue
        

if __name__ == "__main__":
    client = MECClient()
    if client.connect():
        client.start_service("ebukaamadiobi/knn-model")
    else:
        print("Failed to connect to the server.")