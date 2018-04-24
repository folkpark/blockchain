'''
Author: Parker Folkman
Date: 4/24/2018

'''

import socket
import threading
import time
import sys
import pickle


def serverThread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        serversocket.bind((ip_dict.get('node1'), 8089))
    elif nodeName == 'node2':
        serversocket.bind((ip_dict.get('node2'), 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(4096)
        if len(buf) > 0:
            print("Read [%s] from buffer",buf)
            break

def clientThread():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        clientsocket.connect((ip_dict.get('node2'), 8089))
    elif nodeName == 'node2':
        clientsocket.connect((ip_dict.get('node1'), 8089))
    clientsocket.send('Ah dude Parker kills it')

if __name__ == "__main__":
    print("hello world")
    threads = []
    nodeName = sys.argv[1]
    ip = ''
    ip_dict = {
        'node1': '10.142.0.10',
        'node2': '10.142.0.11',
        'node3': '10.142.0.12',
        'node4': '10.142.0.13',
    }

    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    clientThread.start()
    time.sleep(2)  # wait two seconds for the connections to be made.