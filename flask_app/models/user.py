import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = 'next_nursery'

ID = 'id'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
USER_NAME = 'user_name'
EMAIL = 'email'
PASS_HASH = 'pass_hash'
CREATED_AT = 'created_at'
UPDATED_AT = 'updated_at'

NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[A-Z]).{8,}$')

class User:
    def __init__(self, data):
        self.id = data[ID]
        self.first_name = data[FIRST_NAME]
        self.last_name = data[LAST_NAME]
        self.user_name = data[USER_NAME]
        self.email = data[EMAIL]
        self.pass_hash = data[PASS_HASH]
        self.created_at = data[CREATED_AT]
        self.updated_at = data[UPDATED_AT]

    @classmethod
    def create(cls, data):
        query = f"INSERT INTO users ({FIRST_NAME}, {LAST_NAME}, {USER_NAME}, {EMAIL}, {PASS_HASH}) VALUES (%({FIRST_NAME})s, %({LAST_NAME})s, %({USER_NAME})s, %({EMAIL})s, %({PASS_HASH})s);"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @staticmethod
    def validate_registration(data):
        is_valid = True

        if not NAME_REGEX.match(data[FIRST_NAME]):
            flash('First name must be at least 2 characters and only letters', 'register')
            is_valid = False

        if not NAME_REGEX.match(data[LAST_NAME]):
            flash('Last name must be at least 2 characters and only letters', 'register')
            is_valid = False

        if not NAME_REGEX.match(data[USER_NAME]):
            flash('Valid user name required', 'register')
            is_valid = False
        elif User.get_by_user_name(data[USER_NAME]): 
            flash('User name already exists', 'register')
            is_valid = False
        
        if not EMAIL_REGEX.match(data[EMAIL]):
            flash('Valid email required', 'register')
            is_valid = False
        elif not data['confirm_email'] == data['email']:
            flash('Emails must match', 'register')
            is_valid = False
        elif User.get_by_email(data[EMAIL]): 
            flash('Account already exists', 'register')
            is_valid = False

        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must be at least 8 characters and contain at least one digit and one capital letter', 'register')
            is_valid = False
        if not data['confirm_password'] == data['password']:
            flash('Passwords must match', 'register')
            is_valid = False

        return is_valid

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(DB_NAME).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_user_name(cls, user_name):
        query = f"SELECT * FROM users WHERE {USER_NAME} = %(user_name)s;"
        data = {
            USER_NAME: user_name
        }
        results = connectToMySQL(DB_NAME).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @classmethod
    def get_by_email(cls, email):
        query = f"SELECT * FROM users WHERE {EMAIL} = %(email)s;"
        data = {
            EMAIL: email
        }
        results = connectToMySQL(DB_NAME).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT * FROM users WHERE {ID} = %(id)s;"
        data = {
            "id": id
        }

        results = connectToMySQL(DB_NAME).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])
