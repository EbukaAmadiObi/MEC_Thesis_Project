import socket

def send_string(s, string):

    print(f"Sending message: '{string}'")
    s.sendall(string.encode())

if __name__=="__main__":
    
    # Create a TCP/IP socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created successfully")

    # Connect to given port
    s.connect(("127.0.0.1", 14000))
    print(f"Socket connected to {'127.0.0.1'} port no. {14000}")

    while True:

        string = input("What message would you like to send?\n")

        test = send_string(s, string)

        if string == "quit":
            print("Closing socket")
            s.close()
            break
    