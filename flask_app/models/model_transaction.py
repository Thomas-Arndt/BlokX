from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
import re

DATABASE='blokx_schema'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Transaction:
    def __init__(self, data):
        if 'id' in data:
            self.id=data['id']
        if 'sender' in data:
            self.sender=data['sender']
        if 'receiver' in data:
            self.receiver=data['receiver']
        if 'amount' in data:
            self.amount=data['amount']
        if 'message' in data:
            self.message=data['message']
        if 'received_amount' in data:
            self.received_amount=data['received_amount']
        if 'sent_amount' in data:
            self.sent_amount=data['sent_amount']
        self.timestamp=datetime.now()
    
    def serialize_txn(self):
        serialized_txn=f"sender: {self.sender} - receiver: {self.receiver} - amount: {str(self.amount)} - timestamp: {str(self.timestamp)}"
        return serialized_txn
    
    # C
    @classmethod
    def create_transaction(cls, data:dict) -> int:
        query="INSERT INTO transactions (sender_id, receiver_id, amount, message) VALUES (%(sender_id)s, %(receiver_id)s, %(amount)s, %(message)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def create_deposit(cls, data:dict) -> int:
        query="INSERT INTO transactions (sender_id, receiver_id, amount, message) VALUES (%(sender_id)s, %(receiver_id)s, %(amount)s, %(message)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # R
    @classmethod
    def get_one(cls, data:dict) -> list:
        query="SELECT * FROM transactions WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) -> list:
        query="SELECT * FROM transactions;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_transactions = []
            for transaction in results:
                all_transactions.append(cls(transaction))
            return all_transactions
        return False
    
    @classmethod
    def get_sum_of_transaction_as_sender(cls, data) -> list:
        query="SELECT SUM(amount) AS sent_amount FROM transactions WHERE sender_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results[0]['sent_amount'] != None:
            return results[0]
        else:
            return {"sent_amount":0}
        return False
    
    @classmethod
    def get_sum_of_transaction_as_receiver(cls, data) -> list:
        query="SELECT SUM(amount) AS received_amount FROM transactions WHERE receiver_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results[0]['received_amount'] != None:
            return results[0]
        else:
            return {"received_amount":0}
        return False

    # U
    @classmethod
    def update_one(cls, data:dict) -> None:
        query="UPDATE transactions SET sender_id=%(sender_id)s, receiver_id=%(receiver_id)s, amount=%(amount)s, message=%(message)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query="DELETE FROM transactions WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
