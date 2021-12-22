from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import CHAIN
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
        
        if not Miner.get_txn_backup():
            # create txn backup
            self.pending_txns=[]
            frozen=jsonpickle.encode(self.pending_txns)
            backup_id=Miner.create_txn_backup(frozen)
            query="UPDATE pending_transactions_backup SET id=1 WHERE id=%(id)s;"
            connectToMySQL(DATABASE).query_db(query, {"id":backup_id})
        else:
            # Get txn backup
            frozen=Miner.get_txn_backup()
            self.pending_txns=jsonpickle.decode(frozen['txn'])

        print("Miner instantiated!")

        self.thread=threading.Thread(target=self.mine, args=(7,))
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

            self.pending_txns=[]
            frozen=jsonpickle.encode(self.pending_txns)
            Miner.update_txn_backup({"pending_txns":frozen})


    def add_new_transaction(self, new_tx):
        self.pending_txns.append(new_tx)

        print("******PENDING TRANSACTIONS******")
        print(self.pending_txns)
        print("********************************")

        frozen=jsonpickle.encode(self.pending_txns)
        Miner.update_txn_backup({"pending_txns":frozen})

        self.block.merkle_root=MerkleTree(self.pending_txns).merkle_root()
        self.block.nonce=0

    def get_pending_sent_amount(self, user=None):
        sent_amount=0
        if user == None:
            return None
        else:
            txns_sender=[txn.amount for txn in self.pending_txns if txn.sender == user]
            # print(txns_sender)
            for txn in txns_sender:
                if txn:
                    sent_amount+=float(txn)
        # print(sent_amount)
        return sent_amount
    
    # C
    @classmethod
    def create_txn_backup(cls, pending_txns):
        query="INSERT INTO pending_transactions_backup (txn) VALUES (%(pending_txns)s);"
        return connectToMySQL(DATABASE).query_db(query, {"pending_txns":pending_txns})
    
    # R
    @classmethod
    def get_txn_backup(cls):
        query="SELECT * FROM pending_transactions_backup;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            return results[0]
        return False
    
    # U
    @classmethod
    def update_txn_backup(cls, data):
        query="UPDATE pending_transactions_backup SET txn=%(pending_txns)s WHERE id=1;"
        return connectToMySQL(DATABASE).query_db(query, data, show_query=False)



