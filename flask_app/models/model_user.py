from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DATABASE='blokx_schema'


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    # C
    @classmethod
    def create(cls, data:dict) -> int:
        query="INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # R
    @classmethod
    def get_one(cls, data:dict) -> list:
        query="SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_user_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls) -> list:
        query="SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    # U
    @classmethod
    def update_one(cls, data:dict) -> None:
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_user_password(cls, data:dict) -> None:
        query="UPDATE users SET password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # D
    @classmethod
    def delete_one(cls, data:dict) -> None:
        query="DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    # ***************Validations*****************

    @staticmethod
    def validate_registration(data):
        is_valid=True

        # Check First Name Field
        if not data['first_name'] or len(data['first_name']) < 2:
            flash("Please enter your first name.", "err_first_name")
            is_valid=False
        
        # Check Last Name Field
        if not data['last_name'] or len(data['last_name']) < 2:
            flash("Please enter your last name.", "err_last_name")
            is_valid=False
        
        # Check Email Field
        if not data['email'] or not EMAIL_REGEX.match(data['email']):
            flash("Please enter a valid email address.", "err_email")
            is_valid=False

        query="SELECT email from users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            for email in results:
                if data['email'] == email['email']:
                    flash("Please enter a valid email.", "err_email")
                    is_valid=False

        # Check Password Field
        if not data['password']:
            flash("Please enter a password.", "err_password")
            is_valid=False
        
        elif not PASSWORD_REGEX.match(data['password']):
            flash("Password must be at least 8 letters, and must include at least one lowercase letter, one uppercase letter, and one number.", "err_password")
            is_valid=False

        # Check Confirm Password Field
        if not data['password_confirm']:
            flash("Please retype your password.", "err_password_confirm")
            is_valid=False

        elif data['password'] != data['password_confirm']:
            flash("Passwords do not match.", "err_password_confirm")
            is_valid=False

        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid=True
        # Check Email Field
        if not data['email']:
            flash("Please enter your email.", "err_email")
            is_valid=False

        elif not EMAIL_REGEX.match(data['email']):
            flash("Please enter a valid email.", "err_email")
            is_valid=False
        
        # Check if email is in database
        else:
            user_in_db = User.get_user_by_email(data)
            if not user_in_db:
                flash("Please enter a valid email.", "err_email")
                is_valid=False
        

        # Check password Field
        if not data['password']:
            flash("Please enter a valid password.", "err_login")
            is_valid=False


        return is_valid
    
    @staticmethod
    def validate_password_change(data):
        is_valid=True
        # Check Old Password Field
        if not data['old_password']:
            flash("Please provide your current password.", "err_old_password")
            is_valid=False
        
        # Check New Password Field
        if not data['new_password']:
            flash("Please enter a password.", "err_new_password")
            is_valid=False
        
        elif not PASSWORD_REGEX.match(data['new_password']):
            flash("Password must be at least 8 letters, and must include at least one lowercase letter, one uppercase letter, and one number.", "err_new_password")
            is_valid=False

        # Check Confirm Password Field
        if not data['password_confirm']:
            flash("Please retype your password.", "err_password_confirm")
            is_valid=False

        elif data['new_password'] != data['password_confirm']:
            flash("Passwords do not match.", "err_password_confirm")
            is_valid=False
        
        return is_valid