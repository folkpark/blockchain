'''
Author: Parker Folkman
Date: 4/24/2018
Overview: This is a Modified Proof of Stake blockchain that resolves
the lazy miner problem as well as the rich get richer problem. This code
was written as a programming assignment in CSCI 520 Distributed Systems at 
Montana State University. This code is free for anyone to use at your discretion. This software comes
As-Is with no warranties guaranteed or implied. 

Please see the Readme for the assignment prompt for the specifications that this code addresses. 

'''

import socket
import threading
import time
import datetime
import sys
import pickle
from block import Block

def writeToLog(logEntry):
    file = open("log.txt", "a")
    #write the log out to a file
    file.write('\n')
    file.write(logEntry)
    file.close()

# block strings need to be of the form:
# "block;blockNum;trans|sender|receiver|amount;timestamp;signature1|signature2"
def parseBlock(block_str):
    blockValues = block_str.split(";")
    blockNum = blockValues[1]

    transaction_str = blockValues[2]
    trans_temp = transaction_str.split("|")
    sender = trans_temp[1]
    receiver = trans_temp[2]
    amount = trans_temp[3]
    trans_L = [sender,receiver,amount]

    timestamp = blockValues[3]

    signatures_str = blockValues[4]
    signatures_L = signatures_str.split("|")

    newblock = Block(blockNum,trans_L,timestamp,signatures_L)
    return newblock

def parseTransaction(transaction_str):
    values = transaction_str.split("|")
    sender = values[1]
    receiver = values[2]
    amount = values[3]
    transaction_L = [sender,receiver,amount]
    return transaction_L

def createTransaction():
    spender = input("Who is spending?: ")
    receiver = input("Who is receiving?: ")
    amount = input("What is the amount?: ")
    transaction = "trans|%s|%s|%s" % (spender,receiver,amount)
    return transaction

def getTurn():
    return len(blockchain)%4

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
            msgValues = msg.split(";")
            msgType = msgValues[0]
            if msgType == 'ACK':
                print("ACK received %s" % (msg))
            elif msgType == 'printChain':
                printBlockchain()
            elif msgType == 'trans':
                thisNodeTurn = turn_dict.get(nodeName)
                currentTurn = getTurn()
                if thisNodeTurn == currentTurn:
                    print("My turn to create a block!")
            else:
                print("Read [%s] from buffer" % (msg))
                #check if its a good transaction
                # if its a bad transaction do nothing
                # if its a good transaction, create a block > sign block
                    # a. create a block
                    # b. sign the block
                    # c. prepare the block for sending
                    # d. send the block to the other nodes
                serverSendMsgToAll("ACK")
# End Server thread

# def prepareBlock(block):
#

def serverSendMsgToAll(msg):
    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    p = pickle.dumps(msg)
    clientsocket1.send(p)
    clientsocket2.send(p)
    clientsocket3.send(p)

def clientSendToAll(transaction):
    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientsocket1.connect((ip_dict.get('node1'), 5000))
    clientsocket2.connect((ip_dict.get('node2'), 5000))
    clientsocket3.connect((ip_dict.get('node3'), 5000))
    clientsocket4.connect((ip_dict.get('node4'), 5000))

    p = pickle.dumps(transaction)
    clientsocket1.send(p)
    clientsocket2.send(p)
    clientsocket3.send(p)
    clientsocket4.send(p)

#Client Thread
def clientThread():
    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def printBlockchain():
    print()
    for block in blockchain:
        print("***************************************")
        print("Block Number: %s" % (block.blockNumber))
        print("Block Transactions: %s" % (block.transactions))
        print("Block Timestamp: %s" % (block.timestamp))
        print("Block Signatures: %s" % (block.signatures))
        print("***************************************")
        print("     |     ")
        print("     |     ")
        print("     V     ")
    print()

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

    turn_dict = {
        'node1': 0,
        'node2': 1,
        'node3': 2,
        'node4': 3
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

    if nodeName != 'client':
        serverThread = threading.Thread(target=serverThread)
        threads.append(serverThread)
        clientThread = threading.Thread(target=clientThread)
        threads.append(clientThread)
        serverThread.start()
        time.sleep(3)  # let the server thread have time to start on all nodes
        clientThread.start()
    else:
        while True:
            print("Enter integer selection (q to quit)")
            print("Create Transaction 1:")
            print("View Blockchain 2:")
            print("View Ledger 3: ")
            n = input("Please enter selection: ")

            if n is '1':
                print()
                transaction = createTransaction()
                print(transaction)
                clientSendToAll(transaction)
            elif n is '2':
                clientSendToAll("printChain")
            elif n is '3':
                print("Print Ledger")
            elif n is 'q':
                break