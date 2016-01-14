#!/usr/bin/env python3
# PeterMaarNetworkedChatClientGUI.py

from tkinter import *
import socket
import time

__author__ = 'Peter Maar'
__version__ = '1.0.0'

msg = ''
lastReceive = ''

exitmode = False
instantmode = False

def send(ip, port, message):
    global exitmode
    udp_ip = ip
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    try:
        sock.sendto(bytes(message, "utf-8"), (udp_ip, udp_port))
    except socket.gaierror:
        labelText.set("Error. Cannot find host.")
        entryText.set('Select this and press enter to exit.')
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        exitmode = True
        return "exit"
    except OverflowError:
        labelText.set("Error. Bad port number. Invalid port number. Port too high.")
        entryText.set('Select this and press enter to exit.')
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        exitmode = True
        return "exit"

    sock.close()


def receive(port):
    global exitmode
    udp_ip = ''
    udp_port = port

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    try:
        sock.bind((udp_ip, udp_port))
    except PermissionError:
        labelText.set("Error. Bad port number. Permission denied. Port too low.")
        entryText.set('Select this and press enter to exit.')
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        exitmode = True
        return "exit"
    except OSError:
        labelText.set("Error. You seem to be running the client on the same computer as the server.\nUnfortunately this doesn't work.\nIf you want a workaround for testing, try running one from a VM with a bridged adapter.")
        entryText.set('Select this and press enter to exit.')
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        exitmode = True
        return "exit"
    
    sock.settimeout(5)
    try:
        data, addr = sock.recvfrom(268435456) # buffer size is 1/4 GB
    except socket.timeout:
        return "timeout\n\n\n:::\n\n\ntry again"
        
    recievedMessage = data.decode("utf-8")
    sock.close()
    return recievedMessage


def sendAndRecieveText(textEntered):
    """Sends the message in 'textEntered' and return what was recieved. If timeout, returns 'timeout\n\n\n:::\n\n\ntry again' if timeout multiple times returns 'timeout\n\n\n:::\n\n\ngive up'"""
    global exitmode
    global lastReceive
    if send(srvrIp, srvrPort, lastReceive + "\n\n\n:::\n\n\n" + textEntered) == "exit":
        return "exit"
    lr = receive(srvrPort)
    if lr == "exit" and exitmode:
        return "exit"
    elif lr != "timeout\n\n\n:::\n\n\ntry again":
        lastReceive = lr

    # If receive(srvrPort) times out, it returns 'timeout\n\n\n:::\n\n\ntry again'
    tryCount = 0
    while lr == "timeout\n\n\n:::\n\n\ntry again":
        if tryCount < 3:
            if send(srvrIp, srvrPort, lastReceive + "\n\n\n:::\n\n\n" + textEntered) == "exit":
                return "exit"
            lr = receive(srvrPort)
        else:
            return "timeout\n\n\n:::\n\n\ngive up"
        tryCount += 1
    lastReceive = lr

    #time.sleep(len(lastReceive)/10)  # Wait to make it seem like the bot is 'typing'
    return lastReceive

root = Tk()

labelText = StringVar()
l = Label(root, textvariable=labelText)
l.pack()


entryText = StringVar()
e = Entry(root, textvariable=entryText, width=100)
e.pack()

gettingIP = True
labelText.set("Enter the server's IP address or hostname:")


def returnKey(event):  # When the user hits enter,
    global instantmode
    global exitmode
    global gettingIP
    global gettingPort
    global srvrIp
    global srvrPort
    if exitmode:
        entryText.set("Bye! Program should now exit. If it doesn't, close this window.")
        root.update()
        time.sleep(1)
        exit()
    if gettingIP:
        srvrIp = e.get()
        entryText.set('')
        gettingIP = False
        gettingPort = True
        labelText.set("Enter the server's port number:")
    elif gettingPort:
        try:
            srvrPort = int(e.get())
        except ValueError:
            labelText.set("Error. Port must be an integer.")
            root.update()
            entryText.set('Select this and press enter to exit.')
            root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
            exitmode = True
            return None # Method doesn't return anything anyways, and this will make it exit the method without continuing
        entryText.set('')
        labelText.set("Enter a message below to start the conversation.")
        gettingPort = False
    else:
        textEntered = e.get()
        entryText.set('')  # Clear the input box,
        if textEntered == "instantmode: on": # Enable instantmode
            instantmode = True
            return None # Get out of the function so nothing is sent
        elif textEntered == "instantmode: off": # Disable instantmode
            instantmode = False
            return None # Get out of the function so nothing is sent
        labelText.set("Sending and waiting for response...")
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        botReply = sendAndRecieveText(textEntered)
        if botReply == "exit":
            return None
        if botReply == "timeout\n\n\n:::\n\n\ngive up":
            labelText.set("Error. Cannot connect to server.")
            entryText.set('Select this and press enter to exit.')
            root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
            exitmode = True
            return None # Method doesn't return anything anyways, and this will make it exit the method without continuing
        if not instantmode:
            time.sleep(len(textEntered)/3)
        labelText.set("User is typing...")
        root.update()  # 'root' won't automatically update until the method finishes, so to change it while it runs, we need to call 'root.update()'
        if not instantmode:
            time.sleep(len(botReply)/10)
        labelText.set(botReply)
e.bind('<Return>', returnKey)

root.title("Peter Maar's Networked Learning Chatbot - Client GUI")

root.lift()

root.mainloop()
