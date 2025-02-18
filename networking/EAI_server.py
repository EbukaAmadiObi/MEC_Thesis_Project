import socket

class EAIServer:
    
    def __init__(self, ip = "127.0.0.1", port = 14000, verbose = True):
        
        self.ip = ip
        self.port = port
        self.verbose = verbose
        self.is_connected = False

    def listen(self):
        """Listen for connections given address

        Args:
            ip (str, optional): IP of server, defaults to localhost. Defaults to "127.0.0.1".
            port (int, optional): Port to listen on. Defaults to 14000.
            verbose (bool, optional): Turn on print statements. Defaults to True.

        Returns:
            connection, address: (connection object, address tuple)
        """

        # Create a TCP/IP socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.verbose: print("Socket created successfully")

        # Bind to given port
        s.bind((self.ip, self.port))
        if self.verbose: print(f"Socket bound to port no. {self.port}")

        # Listen for incoming connections on given socket
        s.listen(5)
        if self.verbose: print(f"Listening...")

        # When found, create connection object and string for received text
        # TODO: Set up keyboard interrupt for listening, doesnt jump out - timeout periodically?
        connection, addy = s.accept()

        if self.verbose: print(f"Accepted connection with {addy}")

        self.is_connected = True

        return connection, addy

    def recv_str(self, buffer_size = 16):
        """Receive string from client

        Args:
            connection (socket.connection): connection object with client
            buffer_size (int, optional): Buffer size for communication. Defaults to 16.
            verbose (bool, optional): Turn on print statements. Defaults to True.

        Returns:
            str: Received string
        """

        received_string = ""
        while True:
                byte_block = self.connection.recv(buffer_size)
                string_block = byte_block.decode()
                received_string+=string_block
                if len(byte_block)<buffer_size:
                    break
        if received_string == "":
            self.is_connected = False
        if self.verbose: print(f"Received string: {received_string}")

        return received_string
        
        
    def send_str(self, str):
        """Send string to client

        Args:
            connection (socket.connection): connection object with client
            str (str): string to send to client
            verbose (bool, optional): turn on print statements. Defaults to True.
        """
        try:
            self.connection.sendall(str.encode())
        except ConnectionResetError:
            self.is_connected = False
            return
        
        if self.verbose: print(f"Sent string: {str}")

    def listen_loop(self):
        while True:
            self.connection, _ = self.listen()

            while self.is_connected:
                received_string = self.recv_str()

                match received_string:
                    case "list":
                        self.send_str("knn - K nearest neighbour")
                    case "knn":
                        print("TODO - spin up docker container and run knn stuff")
            
            print("Ended connection.\n")


if __name__=="__main__":
    server = EAIServer()

    server.listen_loop()
        
