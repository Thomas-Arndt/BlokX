from flask_app import app, CHAIN
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt

from flask_app.config._miner_init import MINER
from flask_app.models.model_user import User
from flask_app.models.model_transaction import Transaction


bcrypt=Bcrypt(app)

@app.route('/users/logout')
def users_logout():
    del session['uuid']
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def users_login():
    data = {
        **request.form
    }

    if not User.validate_login(data):
        return redirect('/')
    
    user_in_db = User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Pasword", "err_login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, data['password']):
        flash("Invalid Email/Pasword", "err_login")
        return redirect('/')
    
    session['uuid'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/register')
def users_new():
    return render_template("register.html")

@app.route('/users/create', methods=['POST'])
def users_create():
    if not User.validate_registration(request.form):
        return redirect('/register')
    
    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        "password": password_hash
    }

    session['uuid'] = User.create(data)
    return redirect('/dashboard')

@app.route('/dashboard')
def users_dashboard():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=MINER.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    # sent_amount=Transaction.get_sum_of_transaction_as_sender({"id":session['uuid']})
    # received_amount=Transaction.get_sum_of_transaction_as_receiver({"id":session['uuid']})
    # balance=received_amount['received_amount']-sent_amount['sent_amount']
    return render_template("welcome.html", user=user, balance=balance)

@app.route('/send')
def users_send():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=MINER.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    # sent_amount=Transaction.get_sum_of_transaction_as_sender({"id":session['uuid']})
    # received_amount=Transaction.get_sum_of_transaction_as_receiver({"id":session['uuid']})
    # balance=received_amount['received_amount']-sent_amount['sent_amount']
    return render_template("send.html", user=user, balance=balance)

@app.route('/deposit')
def users_deposit():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=MINER.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    # sent_amount=Transaction.get_sum_of_transaction_as_sender({"id":session['uuid']})
    # received_amount=Transaction.get_sum_of_transaction_as_receiver({"id":session['uuid']})
    # balance=received_amount['received_amount']-sent_amount['sent_amount']
    return render_template("deposit.html", user=user, balance=balance)

@app.route('/history')
def users_history():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=MINER.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    verified_txns=CHAIN.get_transactions_by_user(user.email)
    print(verified_txns[0])
    # sent_amount=Transaction.get_sum_of_transaction_as_sender({"id":session['uuid']})
    # received_amount=Transaction.get_sum_of_transaction_as_receiver({"id":session['uuid']})
    # balance=received_amount['received_amount']-sent_amount['sent_amount']
    return render_template("transactions.html", user=user, balance=balance, verified_txns=verified_txns)

@app.route('/settings')
def users_settings():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=MINER.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    # sent_amount=Transaction.get_sum_of_transaction_as_sender({"id":session['uuid']})
    # received_amount=Transaction.get_sum_of_transaction_as_receiver({"id":session['uuid']})
    # balance=received_amount['received_amount']-sent_amount['sent_amount']
    return render_template("account_settings.html", user=user, balance=balance)

@app.route('/users/<int:id>/update', methods=['POST'])
def users_update(id):
    return redirect('/')

# @app.route('/users/<int:id>/delete')
# def users_delete(id):
#     return redirect('/')