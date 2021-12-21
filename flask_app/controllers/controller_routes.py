from flask_app import app
from flask import render_template, redirect, session, request
from datetime import datetime
import random
import json

from flask_app.config._miner_init import MINER
from flask_app.models.model_transaction import Transaction

@app.route('/')
def index():
    return render_template("login.html")

# @app.errorhandler(404)
# def server_error(e):
#     print("Running error function...")
#     return render_template("error.html")