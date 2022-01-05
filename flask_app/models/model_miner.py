from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config._blockchain_init import CHAIN
from flask_app.models.model_block import Block
from flask_app.models.model_merkle_tree import MerkleTree
from flask_app.models.model_blockchain import Blockchain
from datetime import datetime
import threading
import jsonpickle


DATABASE="blokx_schema"

class Miner:
    def __init__(self):
        self.merkle_root=""

        print("Miner instantiated!")
        self.thread=threading.Thread(target=self.mine, args=(6,))
        self.thread.daemon=True
        self.thread.start()
        
    def mine(self, difficulty):
        while True:
            self.difficulty=difficulty

            self.merkle_root=MerkleTree().merkle_root()
            self.block=Block(len(CHAIN.chain)+1, datetime.now(), self.merkle_root, 0, CHAIN.chain[-1].own_hash, self.difficulty)

            print("*****************************")
            print("Mining: Started at " + str(datetime.now()))
            print("*****************************")
            while self.block.hash_block()[:self.block.difficulty] != '0'*self.block.difficulty:
                self.block.nonce+=1
            
            for txn in CHAIN.pending_txns:
                self.block.txns.append(txn)
            self.block.own_hash=self.block.hash_block()
            CHAIN.add_block(self.block)

            frozen=jsonpickle.encode(CHAIN)
            Blockchain.update_backup({"blockchain":frozen})
            
            print("*****************************")
            print("PoW Satisfied at "+str(datetime.now()))
            print("*****************************")
            print("#############################")
            print("Header: "+CHAIN.chain[-1].serialize_block_header())
            print("Hash: "+CHAIN.chain[-1].own_hash)
            print(f"Transactions: {CHAIN.chain[-1].txns}")
            print("#############################")

            CHAIN.pending_txns=[]
            frozen=jsonpickle.encode(CHAIN.pending_txns)
            Blockchain.update_txn_backup({"pending_txns":frozen})

    def set_merkle_root(self):
        self.block.merkle_root=MerkleTree().merkle_root()
        return self

    def reset_nonce(self):
        self.block.nonce=0
        return self

    
    
    
    



