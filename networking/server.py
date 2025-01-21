import socket

def listen(ip = "127.0.0.1", port = 14000, verbose =True):
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
    if verbose: print("Socket created successfully")

    # Bind to given port
    s.bind((ip, port))
    if verbose: print(f"Socket bound to port no. {port}")

    # Listen for incoming connections on given socket
    s.listen(5)
    if verbose: print(f"Listening...")

    # When found, create connection object and string for received text
    connection, addy = s.accept()
    if verbose: print(f"Accepted connection with {addy}")

    return connection, addy

def recv_str(connection, buffer_size = 16, verbose = True):
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
            byte_block = connection.recv(buffer_size)
            string_block = byte_block.decode()
            received_string+=string_block
            if len(byte_block)<buffer_size:
                break
    if verbose: print(f"Received string: {received_string}")

    return received_string
    
    
def send_str(connection, str , verbose = True):
    """Send string to client

    Args:
        connection (socket.connection): connection object with client
        str (str): string to send to client
        verbose (bool, optional): turn on print statements. Defaults to True.
    """
    connection.sendall(str.encode())
    if verbose: print(f"Sent string: {str}")


if __name__=="__main__":

    connection, _ = listen()

    while True:
        send_str(connection, "Welcome! What is your message?")
        received_string = recv_str(connection)
        send_str(connection, "Received, thanks!")
