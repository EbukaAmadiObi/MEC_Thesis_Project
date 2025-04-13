"""Socket based MEC server"""

import socket

class MECServer:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        self.running = False
        self.containters = {}
        self.served_socket = None

    def start(self):
        """Start the websocket server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.served_socket.bind((self.host, self.port))
        self.served_socket.listen(5)
        self.running = True

        print(f"Server started on {self.host}:{self.port}")

        try:
            while self.running:
                client_socket, addr = self.served_socket.accept()
                print(f"Connection from {addr}")
        except KeyboardInterrupt:
            print("Server stopped by user")

if __name__ == "__main__":
    server = MECServer()
    server.start()
