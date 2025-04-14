"""Socket based MEC client"""

import socket
import json
import sys
import threading

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
        # Set up socket, spefifying address family and protocol
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

            # Receive ack response when comamnd is received - manage errors
            response = self.receive_json()
            if "error" in response:
                print(f"Error in starting service: {response["error"]}")
                return False
            elif response.get("status") == "starting_service":
                print(f"Server is starting service...")

            # Receive again when service is started
            response = self.receive_json()
            if "error" in response:
                print(f"Error in starting service: {response["error"]}")
                return False
            elif response.get("status") == "service_started":
                print(f"Service started successfully with container name \"{response["name"]}\"")
                return True
            
            print(f"Unexpected response: {response}")
            return False

        except Exception as e:
            print(f"Exception occurred while sending start command: {str(e)}")
            return False
        
    def start_stream(self):
        self.running = True

        server_output = threading.Thread(target=self.handle_server_output)
        user_input = threading.Thread(target=self.handle_user_input)

        server_output.daemon = True
        user_input.daemon = True

        server_output.start()
        user_input.start()

        server_output.join()
        user_input.join()

    def handle_server_output(self):
        """Handle output from the server, display to user"""
        try:
            while True:
                data = self.server_socket.recv(4096)
                if not data:
                    print("Connection closed by server")
                    self.running = False
                    break

                # Write container output
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
        except Exception as e:
            print(f"Error receiving container output: {str(e)}")
            self.running = False
    
    def handle_user_input(self):
        """Handle input from the user, sending it to the server"""
        try:
            while True:
                data = sys.stdin.buffer.read1(4096)  # Read available data
                if not data:
                    continue
                
                # Send user input to container via server
                try:
                    self.server_socket.sendall(data)
                except (BrokenPipeError, ConnectionResetError):
                    print("Connection lost")
                    self.running = False
                    break
        except Exception as e:
            print(f"Error sending user input: {str(e)}")
            self.running = False

    def receive_json(self) -> dict[str, str]:     # TODO: add timeout - ATM if data is improperly formatted, client will be stuck in receive loop
        data = b""
        """Receive and parse JSON response from server"""
        # Receive chunks of data until no more is left
        while True:
            chunk = self.server_socket.recv(4096)
            if not chunk:
                print("Connection closed by server")
                return None
            data += chunk
            try:
                return decode_json(data)
            except json.JSONDecodeError:    # If json is imporperly formatted, there is more data to receive
                continue
        
if __name__ == "__main__":
    client = MECClient()
    if client.connect():
        client.start_service("ebukaamadiobi/knn-model")
        client.start_stream()
    else:
        print("Failed to connect to the server.")