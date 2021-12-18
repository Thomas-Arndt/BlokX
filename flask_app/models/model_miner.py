import threading
from datetime import datetime
from flask_app.models.model_merkle_tree import MerkleTree
from flask_app.models.model_blockchain import Blockchain
from flask_app.models.model_block import Block

CHAIN=Blockchain()

class Miner:
    def __init__(self):
        self.merkle_root=""
        self.pending_txns=[]
        print("Miner instantiated!")

        self.thread=threading.Thread(target=self.mine, args=(6,))
        self.thread.daemon=True
        self.thread.start()
        
    def mine(self, difficulty):
        while True:
            self.difficulty=difficulty

            self.merkle_root=MerkleTree(self.pending_txns).merkle_root()
            self.block=Block(len(CHAIN.chain)+1, datetime.now(), self.merkle_root, 0, CHAIN.chain[-1].own_hash, self.difficulty)

            print("*****************************")
            print("Mining: Started at " + str(datetime.now()))
            print("*****************************")
            while self.block.hash_block()[:self.block.difficulty] != '0'*self.block.difficulty:
                self.block.nonce+=1
            
            self.block.txns=self.pending_txns
            self.block.own_hash=self.block.hash_block()
            CHAIN.add_block(self.block)
            
            print("*****************************")
            print("PoW Satisfied at "+str(datetime.now()))
            print("*****************************")
            print("#############################")
            print("Header: "+CHAIN.chain[-1].serialize_block_header())
            print("Hash: "+CHAIN.chain[-1].own_hash)
            print(f"Transactions: {CHAIN.chain[-1].txns}")
            print("#############################")
            self.pending_txns=[]


    def add_new_transaction(self, new_tx):
        self.pending_txns.append(new_tx)
        print("******PENDING TRANSACTIONS******")
        print(self.pending_txns)
        print("********************************")
        self.block.merkle_root=MerkleTree(self.pending_txns).merkle_root()
        self.block.nonce=0



