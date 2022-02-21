from flask_app import app
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, set_access_cookies, unset_jwt_cookies, current_user

from flask_app.models.model_user import User

# Create Routes



# Read Routes


# Update Routes



# Login and Registration Routes

# Register New User
@app.route('/api/users/register', methods=['POST'])
def users_register():
    content = request.get_json()

    validation_results = User.validate_registration(content)
    if not validation_results.is_valid:
        return validation_results, 400

    password_hash = bcrypt.generate_password_hash(content.password)

    data = {
        **content,
        "password": password_hash
    }

    newUser = User.create(data)
    access_token = create_access_token(identity=newUser)
    response = jsonify({'message': 'user registered'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    set_access_cookies(response, access_token)

    return response, 200

# Login User
@app.route("/api/users/login", method=["POST"])
def users_login():
    content = request.get_json()

    validation_results = User.validate_login(content)
    if not validation_results.is_valid:
        return validation_results, 400
    
    user_in_db = User.get_user_by_email(content)

    if not user_in_db:
        if not "login" in validation_results.errors:
            validation_results.errors.login = []
        validation_results.errors.login.append("Invalid email/password.")
        return validation_results, 400
    
    if not bcrypt.check_password_hash(user_in_db.password, content.password):
        if not "login" in validation_results.errors:
            validation_results.errors.login = []
        validation_results.errors.login.append("Invalid email/password.")
        return validation_results, 400
    
    access_token = create_access_token(identity=user_in_db)
    response = jsonify({'message': 'login successful'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    set_access_cookies(response, access_token)

    return response, 200


# Logout User
@app.route('/api/users/logout')
def logout():
    response = jsonify({'message': "logout successful"})
    unset_jwt_cookies(response)
    return response