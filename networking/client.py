import socket

BUFFER_SIZE = 16

# Receive encoded string from server on specified socket s
def recv_string(s):
    received_string = ""
    while True:
        byte_block = s.recv(BUFFER_SIZE)
        string_block = byte_block.decode()
        received_string+=string_block
        if len(byte_block)<BUFFER_SIZE:
            break
    print(f"Server says: {received_string}")

    return received_string

if __name__=="__main__":
    
    # Create a TCP/IP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")

    # Connect to given port
    s.connect(("127.0.0.1", 14000))
    print(f"Socket connected to {'127.0.0.1'} port no. {14000}")

    # Receive opening message from server
    recv_string(s)

    # Prompt message
    string = input("What message would you like to send?\n")

    # Send encoded message
    print(f"Sending message: '{string}'")
    s.sendall(string.encode())

    # Receive confirmation from server
    recv_string(s)
    