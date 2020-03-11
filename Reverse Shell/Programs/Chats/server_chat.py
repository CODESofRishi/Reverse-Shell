# general chat program (server)
import socket
from sys import exit

# creation of socket
i = 3
while i > 0:
    try:
        host = ""
        port = 9999
        sockfd = socket.socket()
        break
    except socket.error as err:
        if i == 1:
            print("Failed to create socket !!!")
            exit()
        print(f"Error in socket: {err}\nRetrying...")
        i -= 1
        continue
# binding socket
i = 3
while i > 0:
    try:
        sockfd.bind((host, port))
        print(f"Binding port {port} to the socket successful.")
        sockfd.listen(5)
        break
    except socket.error as err:
        if i == 1:
            print("Unsuccessful binding or listening !!!")
            exit()
        print(f"Error in binding: {err}\nRetrying...")
        i -= 1
        continue

# accepting connections
conn, address_client = sockfd.accept()
print(
    f"Connection established with {address_client[0]} from port {address_client[1]}.\n")

# sending and receiving commands
while True:
    cmd = input("Enter your command: ")
    if cmd == "quit":
        conn.send(cmd.encode("utf-8"))  # sending in bytes format
        break
    elif len(cmd) > 0:
        conn.send(cmd.encode("utf-8"))  # sending in bytes format
        print("\n-----WAITING FOR CLIENT RESPONSE-----\n")
        # receiving and converting the response in string format
        client_response = conn.recv(1024).decode("utf-8")
        if client_response == "quit":
            print("Client terminated the connection!\nShutting down the server!")
            break
        else:
            print(client_response, end="\n\n")

# terminating the connection
conn.close()
sockfd.close()
