from flask_app import app, MINER
from flask import render_template, redirect, session, request
from datetime import datetime
import random
import json

from flask_app.models.model_transaction import Transaction

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add/txn')
def add_txn():
    # txn={
    #         "sender": "A",
    #         "receiver": "B",
    #         "amount": random.randint(0, 1000),
    #         "timestamp": str(datetime.now())
    #         }
    user_1=f"user{random.randint(0,100)}@email.com"
    user_2=f"user{random.randint(0,100)}@email.com"
    txn=Transaction(user_1, user_2, random.randint(0, 1000), "This is a test transaction.")
    MINER.add_new_transaction(txn)
    return redirect('/')


# @app.errorhandler(404)
# def server_error(e):
#     print("Running error function...")
#     return render_template("error.html")