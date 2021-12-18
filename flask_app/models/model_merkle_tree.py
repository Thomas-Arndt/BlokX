import hashlib
import random

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
            self.data_duplicate.append(str(random.randint(0, 1000)))
            self.data_duplicate.append(str(random.randint(0, 1000)))
        while len(self.data_duplicate)>1:
            if len(self.data_duplicate)%2 != 0:
                self.data_duplicate.append(self.data_duplicate[-1])
            for index in range(0, len(self.data_duplicate), 2):
                leaf_hash1=self.hash(self.data_duplicate.pop(0))
                leaf_hash2=self.hash(self.data_duplicate.pop(0))
                self.data_duplicate.append(self.hash(leaf_hash1+leaf_hash2))
        return self.data_duplicate[0]

    def hash(self, string):
        return hashlib.sha256(string.encode('utf-8')).hexdigest()
