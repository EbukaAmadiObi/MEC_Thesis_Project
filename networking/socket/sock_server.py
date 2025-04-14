"""Socket based MEC server"""

import socket

class MECServer:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        self.running = False
        self.containters = {}
        self.server_socket = None

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
        except KeyboardInterrupt:
            print("Server stopped by user")

if __name__ == "__main__":
    server = MECServer()
    server.start()
