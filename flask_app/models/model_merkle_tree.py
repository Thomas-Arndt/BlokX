from flask_app.config._blockchain_init import CHAIN
import hashlib
import random

from flask_app.models.model_transaction import Transaction

class MerkleTree:
    def __init__(self):
        self.data=[]

        self.localize_data_list()

    def localize_data_list(self):
        for txn in CHAIN.pending_txns:
            self.data.append(txn)
    
    def merkle_root(self):
        if len(self.data) <= 1:
            self.data.append(Transaction({"sender":"user_1", "receiver":"user_2", "amount":random.randint(0, 1000), "message":"This is a test transaction."}))
            self.data.append(Transaction({"sender":"user_2", "receiver":"user_1", "amount":random.randint(0, 1000), "message":"This is a test transaction."}))
        while len(self.data)>1:
            if len(self.data)%2 != 0:
                self.data.append(self.data[-1])
            for index in range(0, len(self.data), 2):
                if isinstance(self.data[0], Transaction):
                    self.data[0] = self.data[0].serialize_txn()
                if isinstance(self.data[1], Transaction):
                    self.data[1] = self.data[1].serialize_txn()
                leaf_hash1=self.hash((self.data.pop(0)))
                leaf_hash2=self.hash((self.data.pop(0)))
                self.data.append(self.hash(leaf_hash1+leaf_hash2))
        return self.data[0]

    def hash(self, string):
        return hashlib.sha256(string.encode('utf-8')).hexdigest()
