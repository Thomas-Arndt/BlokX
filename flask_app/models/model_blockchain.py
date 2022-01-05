from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_block import Block
from datetime import datetime
import jsonpickle

DATABASE='blokx_schema'

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.pending_txns=[]

        self.add_block(self.genesis_block())
        self.chain[0].own_hash=self.chain[0].hash_block()

    def genesis_block(self):
        return Block(0, datetime.now(), "Through Code We Grow.", 0, "0000000000000000000000000000000000000000000000000000000000000000", 0)

    def add_block(self, block):
        self.chain.append(block)

    def get_balance_by_user(self, user=None):
        sent_amount=0
        received_amount=0
        if user == None:
            return None
        else:
            txns_sender=[[txn.amount for txn in block.txns if txn.sender == user] for block in self.chain]
            for txn in txns_sender:
                if txn:
                    sent_amount+=round(float(txn[0]),2)
            txns_receiver=[[txn.amount for txn in block.txns if txn.receiver == user] for block in self.chain]
            for txn in txns_receiver:
                if txn:
                    received_amount+=round(float(txn[0]),2)
        return received_amount-sent_amount
    
    def get_transactions_by_user(self, user=None):
        if user==None:
            return None
        else:
            all_txns_by_user = []
            for block in self.chain:
                for txn in block.txns:
                    # print(txn)
                    if txn.sender == user or txn.receiver == user:
                        all_txns_by_user.append(txn)
        return all_txns_by_user
    
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
    
    def add_new_transaction(self, new_tx):
        self.pending_txns.append(new_tx)

        print("******PENDING TRANSACTIONS******")
        print(self.pending_txns)
        print("********************************")

        frozen=jsonpickle.encode(self.pending_txns)
        Blockchain.update_txn_backup({"pending_txns":frozen})
        

    # C
    @classmethod
    def create_backup(cls, chain):
        query="INSERT INTO blockchain_backup (blockchain) VALUES (%(chain)s);"
        return connectToMySQL(DATABASE).query_db(query, {"chain":chain})
    
    # R
    @classmethod
    def get_backup(cls):
        query="SELECT * FROM blockchain_backup;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            return results[0]
        return False
    
    # U
    @classmethod
    def update_backup(cls, data):
        query="UPDATE blockchain_backup SET blockchain=%(blockchain)s WHERE id=1;"
        return connectToMySQL(DATABASE).query_db(query, data, show_query=False)

    
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
    
    @classmethod
    def reset_txn_backup_id(cls, id):
        query="UPDATE pending_transactions_backup SET id=1 WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, {"id":id})


