import hashlib
import random

from flask_app.models.model_transaction import Transaction

class MerkleTree:
    def __init__(self, data_list):
        self.data=data_list
        self.data_duplicate=[]

        self.localize_data_list()

    def localize_data_list(self):
        for data in self.data:
            self.data_duplicate.append(data)
    
    def merkle_root(self):
        if len(self.data_duplicate) <= 1:
            self.data_duplicate.append(Transaction("user_1", "user_2", random.randint(0, 1000), "This is a test transaction."))
            self.data_duplicate.append(Transaction("user_2", "user_1", random.randint(0, 1000), "This is a test transaction."))
        while len(self.data_duplicate)>1:
            if len(self.data_duplicate)%2 != 0:
                self.data_duplicate.append(self.data_duplicate[-1])
            for index in range(0, len(self.data_duplicate), 2):
                if isinstance(self.data_duplicate[0], Transaction):
                    self.data_duplicate[0] = self.data_duplicate[0].serialize_txn()
                if isinstance(self.data_duplicate[1], Transaction):
                    self.data_duplicate[1] = self.data_duplicate[1].serialize_txn()
                leaf_hash1=self.hash((self.data_duplicate.pop(0)))
                leaf_hash2=self.hash((self.data_duplicate.pop(0)))
                self.data_duplicate.append(self.hash(leaf_hash1+leaf_hash2))
        return self.data_duplicate[0]

    def hash(self, string):
        return hashlib.sha256(string.encode('utf-8')).hexdigest()
