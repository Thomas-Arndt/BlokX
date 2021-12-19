from flask_app import app, MINER
from flask import render_template, redirect, session, request, flash

from flask_app.models.model_transaction import Transaction
from flask_app.models.model_user import User


@app.route('/transactions/new')
def transactions_new():
    return render_template("transactions_new.html")

@app.route('/transactions/create', methods=['POST'])
def transactions_create():
    print(request.form)
    receiver=User.get_user_by_email({"email": request.form['recipient']})
    sender=User.get_one({"id":session['uuid']})
    data={
        "sender_id":session['uuid'],
        "receiver_id":receiver.id,
        "amount":request.form['amount'],
        "message":request.form['message']
    }
    transaction=Transaction.create_transaction(data)
    data={
        "sender":sender.email,
        "receiver":receiver.email,
        "amount":request.form['amount'],
        "message":request.form['message']
    }
    MINER.add_new_transaction(Transaction(data))
    return redirect('/send')

@app.route('/deposit/create', methods=['POST'])
def deposit_create():
    print(request.form)
    data={
        "sender_id":1,
        "receiver_id":session['uuid'],
        "amount":request.form['amount'],
        "message":f"Deposit from {request.form['bank_account']} Account"
    }
    transaction=Transaction.create_deposit(data)
    return redirect('/deposit')

@app.route('/transactions/<int:id>')
def transactions_show(id):
    return render_template("transactions_show.html")

@app.route('/transactions/<int:id>/edit')
def transactions_edit(id):
    return render_template("transactions_edit.html")

@app.route('/transactions/<int:id>/update', methods=['POST'])
def transactions_update(id):
    return redirect('/')

@app.route('/transactions/<int:id>/delete')
def transactions_delete(id):
    return redirect('/')