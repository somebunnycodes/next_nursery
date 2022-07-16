import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = 'next_nursery'

ID = 'id'
TITLE = 'title'
PRICE = 'price'
BRAND_NAME = 'brand_name'
BRAND_ID = 'brand_id'
IMAGE_ID = 'image_id'
SELLER_NAME = 'seller_name'
SELLER_ID = 'seller_id'
DESCRIPTION = 'description'
CREATED_AT = 'created_at'
UPDATED_AT = 'updated_at'

class Listing:
    def __init__(self, data):
        self.id = data[ID]
        self.title = data[TITLE]
        self.price = data[PRICE]
        self.brand_name = data[BRAND_NAME]
        self.brand_id = data[BRAND_ID]
        self.image_id = data[IMAGE_ID]
        self.seller_name = data[SELLER_NAME]
        self.seller_id = data[SELLER_ID]
        self.description = data[DESCRIPTION]
        self.created_at = data[CREATED_AT]
        self.updated_at = data[UPDATED_AT]


    @classmethod
    def list_all_listings(cls):
        query = f"SELECT listings.*, users.user_name as seller_name, brands.name as brand_name FROM listings LEFT JOIN users ON users.id=listings.seller_id LEFT JOIN brands ON brands.id=listings.brand_id GROUP BY listings.id;"
        results = connectToMySQL(DB_NAME).query_db(query)
        print(results)

        listings = []
        
        for listing in results:
            listings.append(cls(listing))
        
        return listings

    @classmethod
    def list_user_listings(cls, user_id):
        query = f"SELECT listings.*, users.user_name as seller_name, brands.name as brand_name FROM listings LEFT JOIN users ON users.id=listings.seller_id LEFT JOIN brands ON brands.id=listings.brand_id WHERE listings.seller_id=%(seller_id)s GROUP BY listings.id;"
        data={
            SELLER_ID: user_id
        }
        results = connectToMySQL(DB_NAME).query_db(query, data)
        print(results)

        listings = []
        
        for listing in results:
            listings.append(cls(listing))
        
        return listings

    @classmethod
    def create_listing(cls, data):
        query = f"INSERT INTO listings ({SELLER_ID}, {TITLE}, {PRICE}, {BRAND_ID}, {IMAGE_ID}, {DESCRIPTION}) VALUES (%({SELLER_ID})s, %({TITLE})s, %({PRICE})s, %({BRAND_ID})s, %({IMAGE_ID})s), %({DESCRIPTION});"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def update_listing(cls, data):
        query = f"UPDATE listings SET {TITLE}=%({TITLE})s, {PRICE}=%({PRICE})s, {BRAND_ID}=%({BRAND_ID})s, {IMAGE_ID}=%({IMAGE_ID})s, {DESCRIPTION}=%({DESCRIPTION})s WHERE id=%({ID})s;"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def delete_listing(cls, id):
        query = f"DELETE FROM listings WHERE {ID}=%({ID})s;"
        data = {
            ID: id
        }
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT listings.*, users.user_name as {SELLER_NAME}, brands.name as {BRAND_NAME} FROM listings LEFT JOIN users ON users.{ID}=listings.{SELLER_ID} LEFT JOIN listings ON listings.brand_id=brands.{ID} WHERE listings.{ID}=%({ID})s;"

        data = {
            ID: id
        }

        results = connectToMySQL(DB_NAME).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @staticmethod
    def validate_create_or_update(data):
        is_valid = True
        
        print(data)

        # title
        if not data[TITLE]:
            flash('Please provide a title', TITLE)
            is_valid = False

        # Price
        if not data[PRICE]:
            flash('Please set a sale price', PRICE)
            is_valid = False

        # Brand is drop down

        # Description
        if not data[DESCRIPTION]:
            flash('Please enter a product descrpition', DESCRIPTION)
            is_valid = False
        
        return is_valid
