import sqlite3

class Model:
    def __init__(self, db_name="database/id_inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table = ''
    
    def create(self, data):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(f':{key}' for key in data.keys())
            sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, data)
            self.conn.commit()
            return True, self.cursor.lastrowid
        
        except sqlite3.IntegrityError as e:
            # print(f"An error occurred: {e}")
            return False, f"An error occurred: {e}"
        
        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return False, f"An unexpected error occurred: {e}"

    def read(self, where_clause=None, params=None):
        try:
            sql = f"SELECT * FROM {self.table}"
            if where_clause:
                sql += f" WHERE {where_clause}"
            self.cursor.execute(sql, params or {})
            rows = self.cursor.fetchall()
            return True, rows
        
        except Exception as e:
            print(f"An error occurred during read operation: {e}")
            return False, f"An error occurred during read operation: {e}"

    def update(self, data, where_clause, params=None):
        try:
            columns = ', '.join(f"{key} = :{key}" for key in data.keys())
            sql = f"UPDATE {self.table} SET {columns} WHERE {where_clause}"
            self.cursor.execute(sql, {**data, **(params or {})})
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError as e:
            # print(f"An error occurred: {e}")
            return False, f"An error occurred: {e}"
        
        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return False, f"An unexpected error occurred: {e}"

    def delete(self, where_clause, params=None):
        try:
            sql = f"DELETE FROM {self.table} WHERE {where_clause}"
            self.cursor.execute(sql, params or {})
            self.conn.commit()
            return True
        
        except Exception as e:
            # print(f"An error occurred during delete operation: {e}")
            return False, f"An error occurred during delete operation: {e}"

    def close_connection(self):
        try:
            self.conn.close()
        except Exception as e:
            print(f"An error occurred while closing the connection: {e}")
