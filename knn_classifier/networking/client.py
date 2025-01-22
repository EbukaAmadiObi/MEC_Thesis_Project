import socket

def connect_to_server(ip = "127.0.0.1", port = 14000, verbose = True):
    """Connect to server at given ip on given port

    Args:
        ip (str): ip address of server
        port (int): port number of server
        verbose (bool, optional): Turn on print statements. Defaults to True.
    """
    # Create a TCP/IP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if verbose: print("Socket created successfully")

    # Connect to given port
    s.connect((ip, port))
    if verbose: print(f"Socket connected to {ip} port no. {port}")

    return s

def recv_str(s, buffer_size = 16, verbose = True):
    """Receive string from server

    Args:
        s (socket.socket): socket to receive string from

    Returns:
        str: Received string
    """
    received_string = ""
    while True:
        byte_block = s.recv(buffer_size)
        string_block = byte_block.decode()
        received_string+=string_block
        if len(byte_block)<buffer_size:
            break
    if verbose: print(f"Received string: {received_string}")

    return received_string

def send_str(s, str, verbose = True):
    
    # Send encoded message
    s.sendall(str.encode())
    if verbose: print(f"Sent message: '{str}'")

if __name__=="__main__":
    
    s = connect_to_server()

    while True:
        # Receive opening message from server
        recv_str(s)

        # Prompt message
        string = input("\n")

        # Send string
        send_str(s, string)

        # Receive confirmation from server
        recv_str(s)
        