# model/model.py

import sqlite3

class Model:
    def __init__(self, db_name="database/id_inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table = ''
    
    def create(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(f':{key}' for key in data.keys())
        sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, data)
        self.conn.commit()

    def read(self, where_clause=None, params=None):
        sql = f"SELECT * FROM {self.table}"
        if where_clause:
            sql += f" WHERE {where_clause}"
        self.cursor.execute(sql, params or {})
        rows = self.cursor.fetchall()
        return rows


    def update(self, data, where_clause, params=None):
        columns = ', '.join(f"{key} = :{key}" for key in data.keys())
        sql = f"UPDATE {self.table} SET {columns} WHERE {where_clause}"
        self.cursor.execute(sql, {**data, **(params or {})})
        self.conn.commit()


    def delete(self, where_clause, params=None):
        sql = f"DELETE FROM {self.table} WHERE {where_clause}"
        self.cursor.execute(sql, params or {})
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
