from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_block import Block
from datetime import datetime

DATABASE='blokx_schema'

class Blockchain:
    def __init__(self):
        self.chain=[]

        self.add_block(self.genesis_block())
        self.chain[0].own_hash=self.chain[0].hash_block()

    def genesis_block(self):
        return Block(0, datetime.now(), "In Code We Trust.", 0, "0000000000000000000000000000000000000000000000000000000000000000", 0)

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

    @classmethod
    def get_backup(cls):
        query="SELECT * FROM blockchain_backup;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            return results[0]
        return False

    @classmethod
    def create_backup(cls, chain):
        query="INSERT INTO blockchain_backup (blockchain) VALUES (%(chain)s);"
        return connectToMySQL(DATABASE).query_db(query, {"chain":chain})
    
    @classmethod
    def update_backup(cls, data):
        query="UPDATE blockchain_backup SET blockchain=%(blockchain)s WHERE id=3;"
        return connectToMySQL(DATABASE).query_db(query, data, show_query=False)


