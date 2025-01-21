import socket

if __name__=="__main__":
    
    # Create a TCP/IP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")

    # Connect to given port
    s.connect(("127.0.0.1", 14000))
    print(f"Socket connected to {'127.0.0.1'} port no. {14000}")

    # Prompt message
    string = input("What message would you like to send?\n")

    # Send encoded
    print(f"Sending message: '{string}'")
    s.sendall(string.encode())

    # Receive confirmation from server in blocks
    received_string = ""
    buffer_size = 16

    while True:
        byte_block = s.recv(buffer_size)
        string_block = byte_block.decode()
        received_string+=string_block
        if len(byte_block)<buffer_size:
            break
    print(f"Received string from server: {received_string}")
    