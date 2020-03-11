# general chat program (client)
import socket
from sys import exit

# creating socket
i = 3
while i > 0:
    try:
        host = "10.5.127.144"
        port = 9999
        sockfd = socket.socket()
        break
    except socket.error as err:
        if i == 1:
            print("Failed to create socket !!!")
            exit()
        print("Error in socket creation: {err}\nRetrying...")
        i -= 1
        continue
# connecting to the server (sending connection request)
try:
    sockfd.connect((host, port))
except ConnectionRefusedError:
    print("Server not online !!!")
    exit()

# receiving/sending commands
while True:
    print("\n-----WAITING FOR SERVER'S RESPONSE-----\n")
    server_response = sockfd.recv(1024).decode("utf-8")
    if server_response == "quit":
        print("Server terminated the connection!\nShutting down the client!")
        break
    else:
        print(server_response, end="\n\n")
        cmd = input("Enter your command: ")
        sockfd.send(cmd.encode("utf-8"))
        if cmd == "quit":
            break
# closing connection
sockfd.close()
