#!/usr/bin/env python3
# ClientTerminal.py

import time
import socket

__author__ = 'Peter Maar'
__version__ = '0.1.0'


def send(ip, port, message):
    udp_ip = ip
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (udp_ip, udp_port))

    sock.close()


def receive(port):
    udp_ip = ''
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.bind((udp_ip, udp_port))

    data, addr = sock.recvfrom(268435456) # buffer size is 1/4 GB
    recievedMessage = data.decode("utf-8")
    sock.close()
    return recievedMessage

srvrIp = input("Enter the IP address or hostname of the server:\n")
srvrPort = int(input("Enter the port number of the server:\n"))

msg = ''
lastReceive = ''
while msg.lower() != 'q':
    msg = input("Enter message to send, or 'q' to quit:\n")
    if msg.lower() == 'q':
        time.sleep(1)
        print("Bye!")
        break
    send(srvrIp, srvrPort, lastReceive + "\n\n\n:::\n\n\n" + msg)
    lastReceive = receive(srvrPort)
    time.sleep(len(lastReceive)/10)  # Wait to make it seem like the bot is 'typing'
    print(lastReceive)
