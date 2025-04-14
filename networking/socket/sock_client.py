"""Socket based MEC client"""

import socket
import json

class MECClient:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        self.running = False
        self.container_id = None
        self.server_socket = None
    
    def connect(self):
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
    
    def send(self, str: str):
        self.server_socket.sendall(json.dumps({"string": str}).encode('utf-8'))
        

if __name__ == "__main__":
    client = MECClient()
    if client.connect():
        print("Client connected successfully.")
        string = input("What to send?\n")
        client.send(string)
    else:
        print("Failed to connect to the server.")