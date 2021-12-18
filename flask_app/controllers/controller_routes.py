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
    txn={
            "sender": "A",
            "receiver": "B",
            "amount": random.randint(0, 1000),
            "timestamp": str(datetime.now())
            }
    MINER.add_new_transaction(json.dumps(txn))
    return redirect('/')


# @app.errorhandler(404)
# def server_error(e):
#     print("Running error function...")
#     return render_template("error.html")