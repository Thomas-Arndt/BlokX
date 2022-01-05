from flask_app import app
from flask_app.config._blockchain_init import CHAIN
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt

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
        flash("Invalid Email/Password", "err_login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, data['password']):
        flash("Invalid Email/Password", "err_login")
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
    pending_sent_amount=CHAIN.get_pending_sent_amount(user.email)
    print(pending_sent_amount)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    balance="{:.2f}".format(balance)
    return render_template("welcome.html", user=user, balance=balance)

@app.route('/send')
def users_send():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=CHAIN.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    balance="{:.2f}".format(balance)
    return render_template("send.html", user=user, balance=balance)

@app.route('/deposit')
def users_deposit():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=CHAIN.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    balance="{:.2f}".format(balance)
    return render_template("deposit.html", user=user, balance=balance)

@app.route('/history')
def users_history():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=CHAIN.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    balance="{:.2f}".format(balance)
    verified_txns=CHAIN.get_transactions_by_user(user.email)
    verified_txns.reverse()
    pending_txns=[]
    for txn in CHAIN.pending_txns:
        pending_txns.append(txn)
    pending_txns.reverse()
    has_pending_txns = False
    for txn in pending_txns:
        if txn.sender == user.email or txn.receiver == user.email:
            has_pending_txns=True
    return render_template("transactions.html", user=user, balance=balance, verified_txns=verified_txns, pending_txns=pending_txns, has_pending_txns=has_pending_txns)

@app.route('/settings')
def users_settings():
    user=User.get_one({"id":session['uuid']})
    pending_sent_amount=CHAIN.get_pending_sent_amount(user.email)
    balance=CHAIN.get_balance_by_user(user.email)-pending_sent_amount
    balance="{:.2f}".format(balance)
    return render_template("account_settings.html", user=user, balance=balance)

@app.route('/users/update/password', methods=['POST'])
def users_update_password():
    print(request.form)
    data={
        **request.form
    }
    if not User.validate_password_change(data):
        return redirect('/settings')
    
    user_in_db=User.get_one({"id":session['uuid']})
    
    if not bcrypt.check_password_hash(user_in_db.password, data['old_password']):
        flash("Incorrect password.", "err_old_password")
        return redirect('/settings')
    
    password_hash = bcrypt.generate_password_hash(request.form['new_password'])

    data = {
        "id":session['uuid'],
        "password": password_hash
    }

    User.update_user_password(data)
    flash("Password Updated!", "msg_password_updated")
    return redirect('/settings')

# @app.route('/users/<int:id>/delete')
# def users_delete(id):
#     return redirect('/')