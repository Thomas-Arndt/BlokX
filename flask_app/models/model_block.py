import hashlib

class Block:
    def __init__(self, index, timestamp, merkle_root, nonce, prev_hash, difficulty):
        self.index=index
        self.timestamp=timestamp
        self.merkle_root=merkle_root
        self.nonce=nonce
        self.prev_hash=prev_hash
        self.difficulty=difficulty
        self.own_hash=""
        self.txns=""

    def hash_block(self):
        return hashlib.sha256(self.serialize_block_header().encode('utf-8')).hexdigest()

    def serialize_block_header(self):
        block_header=str(self.index)+"/"+str(self.timestamp)+"/"+self.merkle_root+"/"+str(self.nonce)+"/"+self.prev_hash+"/"+str(self.difficulty)
        return block_header