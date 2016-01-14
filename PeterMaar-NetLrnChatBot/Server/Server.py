#!/usr/bin/env python3
# Server.py

import socket
import Chatbot  # PyCharm seems to think this is an error, but it seems fine.
import random

__author__ = 'Peter Maar'
__version__ = '0.1.0'

def send(ip, port, message):
    udp_ip = ip
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (udp_ip, udp_port))


def receive(port):
    udp_ip = ''
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    try:
        sock.bind((udp_ip, udp_port))
    except OverflowError:
        print("Error. Bad port number. Invalid port number. Port too high.")
        exit()
    except PermissionError:
        print("Error. Bad port number. Permission denied. Port too low.")
        exit()

    try:
        data, addr = sock.recvfrom(268435456) # buffer size is 1/4 GB
    except KeyboardInterrupt:
        print("Stopping server.")
        exit()
    recievedMessage = data.decode("utf-8")
    # For debugging. print("Received message:", "\"" + recievedMessage + "\"", "from", addr)

    sock.close()

    return (recievedMessage, addr[0])


try:
    srvrPort = int(input("Enter the port number to host the server on:\n"))
except ValueError:
    print("Error. Bad port number. Invalid port number. Port number must be an integer.")
    exit()
print("Your Local IP Address is:")
ipSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipSock.connect(("8.8.8.8",80))  #TODO This is the only way to get the IP accurately regardless of network setups, is to connect to something, but this will fail if there is no internet. Maybe add a try except?
print(ipSock.getsockname()[0])
ipSock.close()

print("Starting server...")
Chatbot.processInput('')  # Chatbot knows not to store blank strings (safeToStore stops them), and this will prompt to create the pickle files if needed

num = random.randint(0, 1000000)

print("Server started. Waiting for connections. Press Ctrl + C to exit.")
while True:
    r = receive(srvrPort)
    msg = r[0]
    ip = r[1]

    if msg[msg.find("\n\n\n:::\n\n\n")+9:] == "server: print code":  # If the user says 'server: print code'
        print(num)  # Print the number on the server screen
        send(ip, srvrPort, "Code is now on server console.")
    elif msg[msg.find("\n\n\n:::\n\n\n")+9:] == "server: exit " + str(num):  # If the user says 'server: exit' and the correct code, exit
        send(ip, srvrPort, "Correct code. Server exiting.")
        exit()
    elif msg.find('server: ') == -1 and msg.find("Code is now on server console.") == -1 and msg.find("Server exiting") == -1:  # As long as it isn't a mistyped server command, process it as chat
        send(ip, srvrPort, Chatbot.processInput(msg))
    else:
        send(ip, srvrPort, "Error.")
