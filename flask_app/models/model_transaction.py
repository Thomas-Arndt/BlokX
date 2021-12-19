from datetime import datetime

class Transaction:
    def __init__(self, sender, receiver, amount, message=""):
        self.sender=sender
        self.receiver=receiver
        self.amount=amount
        self.message=message
        self.timestamp=datetime.now()
    
    def serialize_txn(self):
        serialized_txn=f"sender: {self.sender} - receiver: {self.receiver} - amount: {str(self.amount)} - timestamp: {str(self.timestamp)}"
        return serialized_txn
    
    # def __repr(self):
    #     return self.serialize_txn()