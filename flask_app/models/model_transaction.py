from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
import jsonpickle
import re

from flask_app.models.model_user import User


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

    @staticmethod
    def validate_transaction(data):
        is_valid=True

        # Check Amount Field
        if not data['amount'] or data['amount'] == "":
            flash("Please enter an amount to send.", "err_amount")
            is_valid=False

        elif data['balance'] < float(data['amount']):
            flash("You do not have that much to send.", "err_amount")
            is_valid=False
        
        # Check Recipient Field
        receiver=User.get_user_by_email({"email": data['receiver']})
        if not receiver:
            flash("Please enter a valid email.", "err_receiver")
            is_valid=False
        
        # Check Message Field
        if len(data['message'])>120:
            flash("Message cannot be more than 120 characters.", "err_message")
            is_valid=False
        
        return is_valid
    
    @staticmethod
    def validate_deposit(data):
        is_valid=True

        # Check Amount Field
        if not data['amount']:
            flash("Please enter an amount to deposit.", "err_amount")
            is_valid=False
        elif float(data['amount']) <= 0:
            flash("Please enter an amount greater than zero.", "err_amount")
            is_valid=False
        
        # Check Account Field
        if not data['bank_account'] or data['bank_account'] == "":
            flash("Please choose an account.", "err_account")
            is_valid=False
        
        return is_valid