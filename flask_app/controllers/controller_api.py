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
    newUser = User.create(content)
    access_token = create_access_token(identity=newUser);
    response = jsonify({'message': 'user registered'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    set_access_cookies(response, access_token)

    return response, 200

# Login User


# Logout User
@app.route('/api/users/logout')
def logout():
    response = jsonify({'message': "logout successful"})
    unset_jwt_cookies(response)
    return response