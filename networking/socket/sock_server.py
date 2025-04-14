"""Socket based MEC server"""

import socket
import threading
import json

class MECServer:
    def __init__(self, host: str = "localhost", port: int = 3000):
        self.host = host
        self.port = port
        self.running: bool = False
        self.containters = {}
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
            # Receive 4096 bits from 
            data = client_socket.recv(4096)
            if not data:
                print(f"Received empty data from {client_id}")
                return
            try:
                command = json.loads(data.decode("utf-8"))
                print(f"received command: {str(command)}")

            except json.JSONDecodeError as e:
                print(f"Unexpected error parsing JSON from {client_id}: {str(e)}")
                client_socket.sendall(json.dumps({"error":str(e)}))
        except e:
            print(f"Unexpected error handling client {client_id}: {str(e)}")


if __name__ == "__main__":
    server = MECServer()
    server.start()
