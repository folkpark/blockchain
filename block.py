

class Block:

    def __init__(self, blockNumber, transactions, timestamp ,previousHash, hash):
        self.blockNumber = blockNumber
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = hash
        self.timestamp = timestamp

    def getBlockNum(self):
        return self.blockNumber

    def getTransactions(self):
        return self.transactions

    def getPrevHash(self):
        return self.previousHash

    def getHash(self):
        return self.hash

    def getTimestamp(self):
        return self.timestamp