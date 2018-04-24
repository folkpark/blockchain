'''
Author: Parker Folkman
Date: 4/24/2018

'''

import socket
import threading
import time


def serverThread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(64)
        if len(buf) > 0:
            print("Read [%s] from buffer",buf)
            break

def clientThread():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))
    clientsocket.send('Ah dude Parker kills it')

if __name__ == "__main__":
    print("hello world")

    nodeName = ''
    threads = []
    #port = 5000

    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    clientThread.start()
    time.sleep(2)  # wait two seconds for the connections to be made.