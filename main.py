'''
Author: Parker Folkman
Date: 4/24/2018

'''

import socket
import threading
import time
import sys
import pickle
import block


def serverThread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        serversocket.bind((ip_dict.get('node1'), 5000))
    elif nodeName == 'node2':
        serversocket.bind((ip_dict.get('node2'), 5000))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(4096)
        if len(buf) > 0:
            with open("block.p", 'rb') as file:
                msg = pickle.load(file)
            print("Read [%s] from buffer" %(msg))
            print()
            break

def clientThread():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        clientsocket.connect((ip_dict.get('node2'), 5000))
    elif nodeName == 'node2':
        clientsocket.connect((ip_dict.get('node1'), 5000))

    newBlock = block.Block(4)
    with open("block.p", 'wb') as file:
        p = pickle.dump(newBlock, file)

    clientsocket.send(p)

if __name__ == "__main__":
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
    time.sleep(2)  # let the server thread have time to start
    clientThread.start()