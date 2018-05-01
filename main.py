'''
Author: Parker Folkman
Date: 4/24/2018

'''

import socket
import threading
import time
import datetime
import sys
import hashlib
import pickle
from block import Block

def writeToLog(logEntry):
    file = open("log.txt", "a")
    #write the log out to a file
    file.write('\n')
    file.write(logEntry)
    file.close()

def signBlock(sign_str):
    prehashData = sign_str
    prehash = hashlib.sha3_256(prehashData.encode()).hexdigest().encode()
    hash = hashlib.sha3_256(prehash).hexdigest()
    return hash

# def createTransaction():
#

def serverThread():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        serversocket.bind((ip_dict.get('node1'), 5000))
    elif nodeName == 'node2':
        serversocket.bind((ip_dict.get('node2'), 5000))
    elif nodeName == 'node3':
        serversocket.bind((ip_dict.get('node3'), 5000))
    elif nodeName == 'node4':
        serversocket.bind((ip_dict.get('node4'), 5000))
    serversocket.listen(5)  # server socket maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        buf = connection.recv(4096)
        if len(buf) > 0:
            msg = pickle.loads(buf)
            print("Read [%s] from buffer" %(msg))
            print()

def clientThread():
    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if nodeName == 'node1':
        clientsocket1.connect((ip_dict.get('node2'), 5000))
        clientsocket2.connect((ip_dict.get('node3'), 5000))
        clientsocket3.connect((ip_dict.get('node4'), 5000))
    elif nodeName == 'node2':
        clientsocket1.connect((ip_dict.get('node1'), 5000))
        clientsocket2.connect((ip_dict.get('node3'), 5000))
        clientsocket3.connect((ip_dict.get('node4'), 5000))
    elif nodeName == 'node3':
        clientsocket1.connect((ip_dict.get('node1'), 5000))
        clientsocket2.connect((ip_dict.get('node2'), 5000))
        clientsocket3.connect((ip_dict.get('node4'), 5000))
    elif nodeName == 'node4':
        clientsocket1.connect((ip_dict.get('node1'), 5000))
        clientsocket2.connect((ip_dict.get('node2'), 5000))
        clientsocket3.connect((ip_dict.get('node3'), 5000))
    elif nodeName == 'client':
        clientsocket1.connect((ip_dict.get('node1'), 5000))
        clientsocket2.connect((ip_dict.get('node2'), 5000))
        clientsocket3.connect((ip_dict.get('node3'), 5000))
        clientsocket4.connect((ip_dict.get('node4'), 5000))

    # while True:
    #     print("Enter integer selection (q to quit)")
    #     print("Create Transaction 1:")
    #     print("View Blockchain 2:")
    #     n = input("Please enter selection: ")
    #
    #     if n is '1':
    #         print()
    #         p = pickle.dumps("From: %s" %(nodeName))
    #         clientsocket1.send(p)
    #         clientsocket2.send(p)
    #         clientsocket3.send(p)
    #     elif n is '2':
    #         print("Kindly print the blockchain")
    #     elif n is 'q':
    #         break

    # p = pickle.dumps("From: %s" %(nodeName))
    # clientsocket1.send(p)
    # clientsocket2.send(p)
    # clientsocket3.send(p)

if __name__ == "__main__":
    threads = []
    nodeName = sys.argv[1]

    ip_dict = {
        'node1': '10.142.0.10',
        'node2': '10.142.0.11',
        'node3': '10.142.0.12',
        'node4': '10.142.0.13',
    }

    ledger_dict = {
        'Parker': 100,
        'Mike': 100,
        'Jeff': 100,
        'Bentley': 100,
        'Alice': 100,
        'Bob': 100
    }

    #make sure the log is clear.
    with open('log.txt', 'w'):
        pass

    init_transactions = []
    init_signatures = []
    genesisBlock = Block(0, init_transactions,
                         datetime.datetime.now(),
                         init_signatures)

    blockchain = [genesisBlock]  # List to store our blockchain

    serverThread = threading.Thread(target=serverThread)
    threads.append(serverThread)
    clientThread = threading.Thread(target=clientThread)
    threads.append(clientThread)
    serverThread.start()
    time.sleep(2)  # let the server thread have time to start on all nodes
    clientThread.start()