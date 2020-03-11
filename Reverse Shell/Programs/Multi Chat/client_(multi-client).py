# CLIENT (Multi-Client)

import socket


host = "10.5.127.144"
port = 9999

sockfd = socket.socket()

try:
    sockfd.connect((host, port))
except:
    print("Error in connecting to the server !")

print("\n-----WAITING FOR SERVER CHAT CONNECTION-----\n")
while True:
    try:
        server_response = sockfd.recv(1024).decode("utf-8")
        if server_response == " ":
            sockfd.send(" ".encode("utf-8"))
    except:
        print("SERVER SHUT DOWN !\nSHUTTING DOWN THE CLIENT !")
        break

    if server_response == "Server Connected":
        print("SERVER CONNECTED FOR CHAT.")
        while True:
            print("\n-----waiting for server's reponse-----\n")
            server_response = sockfd.recv(1024).decode("utf-8")
            if server_response == "exit":
                print("SERVER DISCONNECTED FROM CHAT !")
                break
            print(server_response)
            instruction = input("Connected--->Server: ")
            sockfd.send(instruction.encode("utf-8"))

    elif server_response == "quit":
        print("SERVER SHUT DOWN !\nSHUTTING DOWN THE CLIENT !")
        break

    print("\n-----WAITING FOR SERVER CHAT CONNECTION-----\n")
