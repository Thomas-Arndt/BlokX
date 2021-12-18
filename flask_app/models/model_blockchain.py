from flask_app.models.model_block import Block
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain=[]

        self.add_block(self.genesis_block())
        self.chain[0].own_hash=self.chain[0].hash_block()

    def genesis_block(self):
        return Block(0, datetime.now(), "In Code We Trust.", 0, "0000000000000000000000000000000000000000000000000000000000000000", 7)

    def add_block(self, block):
        self.chain.append(block)