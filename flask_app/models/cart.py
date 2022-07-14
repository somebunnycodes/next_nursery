import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = 'next_nursery'

USER_ID = 'user_id'
LISTING_ID = 'listing_id'

class Cart:
    
    @classmethod
    def add_listing_to_cart(cls, data):
        query = f"INSERT INTO carts ({USER_ID}, {LISTING_ID}) VALUES (%({USER_ID})s, %({LISTING_ID})s);"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def remove_listing_from_cart(cls, user_id, listing_id):
        query = f"DELETE FROM carts WHERE {USER_ID}=%({USER_ID})s AND {LISTING_ID}=%({LISTING_ID});"
        data = {
            USER_ID: user_id,
            LISTING_ID: listing_id
        }
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def list_listings_in_cart(cls, user_id):
        query = f"SELECT listings.*, users.user_name as seller_name, brands.name as brand_name FROM listings LEFT JOIN carts ON carts.listing_id=listings.id LEFT JOIN users ON users.id=listings.seller_id LEFT JOIN listings ON listings.brand_id=brands.id GROUP BY listings.id WHERE carts.user_id=%({USER_ID})s;"
        data={
            USER_ID: user_id
        }
        
        results = connectToMySQL(DB_NAME).query_db(query, data)

        listings = []
        
        for listing in results:
            listings.append(cls(listing))
        
        return listings
