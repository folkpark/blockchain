import hashlib

class Block:

    def __init__(self, blockNumber, transactions, timestamp ,signatures):
        self.blockNumber = blockNumber
        self.transactions = transactions
        self.signatures = signatures
        self.timestamp = timestamp

    def signBlock(self, sign_str):
        prehashData = sign_str
        prehash = hashlib.sha3_256(prehashData.encode()).hexdigest().encode()
        hash_signature = hashlib.sha3_256(prehash).hexdigest()
        self.signatures.append(hash_signature)

    def getBlockNum(self):
        return self.blockNumber

    def getTransactions(self):
        return self.transactions

    def getPrevHash(self):
        return self.signatures

    def getTimestamp(self):
        return self.timestamp