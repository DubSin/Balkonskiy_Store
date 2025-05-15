import sqlite3


class DataBase:
    def __init__(self, db):
        self.db = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.db.cursor()
    
    def product_exist_by_name(self, name):
        result = self.cursor.execute("SELECT * FROM `assortment` WHERE name = ?", (name, ))
        return bool(len(result.fetchall()))
    
    def get_product(self, prod_type):
        result = self.cursor.execute("SELECT * FROM `assortment` WHERE type = ?", (prod_type, ))
        return result.fetchall()
    
    def product_exist_by_id(self, prod_id):
        result = self.cursor.execute("SELECT * FROM `assortment` WHERE name = ?", (prod_id, ))
        return bool(len(result.fetchall()))

    def get_by_id(self, prod_id):
        result = self.cursor.execute("SELECT * FROM 'assortment' WHERE id = ?", (prod_id, ))
        return result.fetchone()
    
    def add_product(self, name, price, condition, size, photo, prod_type):
        self.cursor.execute("INSERT INTO 'assortment' ('name', 'price', 'condition', 'size', 'photo', 'type') VALUES (?, ?, ?, ?, ?, ?)", (name, price, condition, size, photo, prod_type))
        return self.db.commit()
    
    def find_matches(self, key):
        result = self.cursor.execute(f"SELECT * FROM 'assortment' WHERE name LIKE '%{key}%'")
        return result.fetchall()
    
    def delete_product(self, name):
        self.cursor.execute("DELETE FROM 'assortment' WHERE name = ?", (name, ))
        return self.db.commit()