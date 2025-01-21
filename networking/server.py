import socket

def receive_string(s, buffer_size = 16):

    # When found, create connection object and string for received text
    connection, _ = s.accept()
    received_string = ""

    # Receive blocks of 16 bytes
    while True:
        byte_block = connection.recv(buffer_size)
        string_block = byte_block.decode()
        received_string+=string_block
        print(f"Received block: {string_block}")
        if len(byte_block)<buffer_size:
            break
    # Close connection
    connection.close()

    return received_string

if __name__=="__main__":

    # Create a TCP/IP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")

    # Bind to given port
    s.bind(("127.0.0.1", 14000))
    print(f"Socket bound to port no. {14000}")

    # Listen for incoming connections on given socket
    s.listen(5)
    print(f"Listening...")

    while True:
        test = receive_string(s)
        if test != "quit":
            print(test)
            print("again!")