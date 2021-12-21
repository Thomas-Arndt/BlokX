from flask_app import app, CHAIN
from flask import render_template, redirect, session, request, flash

from flask_app.config._miner_init import MINER
from flask_app.models.model_transaction import Transaction
from flask_app.models.model_user import User



# @app.route('/transactions/new')
# def transactions_new():
#     return render_template("transactions_new.html")

@app.route('/transactions/create', methods=['POST'])
def transactions_create():
    # print(request.form)
    sender=User.get_one({"id":session['uuid']})
    
    pending_sent_amount=MINER.get_pending_sent_amount(sender.email)
    balance=CHAIN.get_balance_by_user(sender.email)-pending_sent_amount
    data={
        "sender":sender.email,
        # "receiver":receiver.email,
        "receiver":request.form['receiver'],
        "amount":request.form['amount'],
        "message":request.form['message'],
        "balance":balance
    }
    if not Transaction.validate_transaction(data):
        return redirect('/send')
    receiver=User.get_user_by_email({"email": request.form['receiver']})
    data['receiver']=receiver.email
    MINER.add_new_transaction(Transaction(data))
    return redirect('/send')

@app.route('/deposit/create', methods=['POST'])
def deposit_create():
    print(request.form)
    data={**request.form}
    if not Transaction.validate_deposit(data):
        return redirect('/deposit')

    receiver=User.get_one({"id":session['uuid']})
    data={
        "sender":"Deposit",
        "receiver":receiver.email,
        "amount":request.form['amount'],
        "message":request.form['bank_account']
    }
    MINER.add_new_transaction(Transaction(data))
    return redirect('/deposit')

# @app.route('/transactions/<int:id>')
# def transactions_show(id):
#     return render_template("transactions_show.html")

# @app.route('/transactions/<int:id>/edit')
# def transactions_edit(id):
#     return render_template("transactions_edit.html")

# @app.route('/transactions/<int:id>/update', methods=['POST'])
# def transactions_update(id):
#     return redirect('/')

# @app.route('/transactions/<int:id>/delete')
# def transactions_delete(id):
#     return redirect('/')