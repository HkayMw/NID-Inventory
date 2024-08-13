# model/model.py

import sqlite3

class Model:
    def __init__(self, db_name="database/id_inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        pass

    def execute_query(self, query, *params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, *params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, *params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
