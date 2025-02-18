import socket
import cmd

class EAIClientCLI(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to EAIAAS CLI. Type \"help\" for available commands."

    def __init__(self, ip = "127.0.0.1", port = 14000, verbose = True):
        super().__init__()
        self.ip = ip
        self.port = port
        self.verbose = verbose

        self.s = self.connect_to_server()

    def connect_to_server(self):
        """Connect to server at given ip on given port

        Args:
            ip (str): ip address of server
            port (int): port number of server
            verbose (bool, optional): Turn on print statements. Defaults to True.
        """
        # Create a TCP/IP socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.verbose: print("Socket created successfully")

        # Connect to given port
        s.connect((self.ip, self.port))
        if self.verbose: print(f"Socket connected to {self.ip} port no. {self.port}")

        return s

    def recv_str(self, buffer_size = 16):
        """Receive string from server

        Args:
            s (socket.socket): socket to receive string from

        Returns:
            str: Received string
        """
        received_string = ""
        while True:
            byte_block = self.s.recv(buffer_size)
            string_block = byte_block.decode()
            received_string+=string_block
            if len(byte_block)<buffer_size:
                break
        if self.verbose: print(f"Received string: {received_string}")

        return received_string

    def send_str(self, str: str):
        # Send encoded message
        self.s.sendall(str.encode())
        if self.verbose: print(f"Sent message: '{str}'")

    def do_ls(self, arg):
        """List all possible services"""
        if not arg:
            self.send_str("list")
            response = self.recv_str()
            print(response)
        else:
            print("ls doesn't take any arguments, try again.")

if __name__=="__main__":
    client = EAIClientCLI()
    
    client.cmdloop()
        