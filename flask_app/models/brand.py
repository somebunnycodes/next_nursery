import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = 'next_nursery'

ID = "id"
NAME = "name"

class Brand:

    def __init__(self, data):
        self.id = data[ID]
        self.name = data[NAME]
    
    @classmethod
    def list_all_brands(cls):
        query = f"SELECT * FROM brands ORDER BY name;"
        results = connectToMySQL(DB_NAME).query_db(query)
        print(results)

        brands = []
        
        for brand in results:
            brands.append(cls(brand))
        
        return brands
    
    @classmethod
    def get_by_id(cls, id):
        query = f"SELECT * FROM brands WHERE {ID}=%({ID})s;"

        data = {
            ID: id
        }

        results = connectToMySQL(DB_NAME).query_db(query,data)

        if len(results) < 1:
            return False

        return cls(results[0])


