

class Block:

    def __init__(self, blockNumber, transactions, timestamp ,signatures):
        self.blockNumber = blockNumber
        self.transactions = transactions
        self.signatures = signatures
        self.timestamp = timestamp

    def getBlockNum(self):
        return self.blockNumber

    def getTransactions(self):
        return self.transactions

    def getPrevHash(self):
        return self.signatures

    def getTimestamp(self):
        return self.timestamp