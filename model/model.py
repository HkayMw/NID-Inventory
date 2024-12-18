import os
import shutil
import sqlite3
from pathlib import Path

# import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# print(db_path)

class Model:
    # def __init__(self, db_name="database/id_inventory1.db"):
    #     self.conn = sqlite3.connect(db_name)
    #     self.cursor = self.conn.cursor()
    #     self.table = ''
    initial_db = resource_path('database/id_inventory1.db')
    
    # def __init__(self, initial_db="database/id_inventory1.db"):
    def __init__(self, initial_db=initial_db):
        # Determine the initial database path
        self.initial_db = Path(initial_db)
        self.db_path = self.get_database_path()
        
        # Check if the database exists; if not, copy the initial database
        if not Path(self.db_path).exists():
            # Ensure the directory exists
            os.makedirs(Path(self.db_path).parent, exist_ok=True)
            # Copy the initial database file to the destination
            shutil.copy(self.initial_db, self.db_path)
        
        # Connect to the database (this should be outside of the if statement)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.table = ''
    
    def get_database_path(self):
        # Get the user's home directory
        home_directory = Path.home()
        # Define the path for your application's database
        database_path = home_directory / "IDInventoryManager" / "database.db"
        
        # Ensure the directory exists
        os.makedirs(database_path.parent, exist_ok=True)

        return str(database_path)
        
    def custom_query(self, query):
        try:
            self.cursor.execute(query)
            
            # Commit the transaction for modification queries
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'REPLACE')):
                self.conn.commit()  # Commit the changes to the database
                return True, 'Operation was successful', None
            
            # Fetch results for SELECT queries
            rows = self.cursor.fetchall()
            return True, 'Operation was successful', rows

        except Exception as e:
            return False, f"An error occurred: {e} from {__name__}", None
    
    def create(self, data):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(f':{key}' for key in data.keys())
            sql = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, data)
            self.conn.commit()
            return True, 'Record created successfully', self.cursor.lastrowid
        
        except sqlite3.IntegrityError as e:
            # print(f"An error occurred: {e}")
            return False, f"An error occurred: {e} from {__name__}", None
        
        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return False, f"An unexpected error occurred: {e} from {__name__}", None

    def read(self, where_clause=None, params=None, order_by=None, order_type=None):
        try:
            sql = f"SELECT * FROM {self.table}"
            if where_clause:
                sql += f" WHERE {where_clause}"
            if order_by and order_type:
                sql += f" ORDER BY {order_by} {order_type}"
            self.cursor.execute(sql, params or {})
            rows = self.cursor.fetchall()
            return True, 'Read operation was successfull', rows
        
        except Exception as e:
            print(f"An error occurred during read operation: {e} from {__name__}")
            return False, f"An error occurred during read operation: {e} from {__name__}", None

    def update(self, data, where_clause, params=None):
        try:
            columns = ', '.join(f"{key} = :{key}" for key in data.keys())
            sql = f"UPDATE {self.table} SET {columns} WHERE {where_clause}"
            self.cursor.execute(sql, {**data, **(params or {})})
            self.conn.commit()
            return True, "Updated Successfully", None
            
        except sqlite3.IntegrityError as e:
            # print(f"An error occurred: {e}")
            return False, f"An error occurred: {e} from {__name__}", None
        
        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return False, f"An unexpected error occurred: {e} from {__name__}", None

    def delete(self, where_clause, params=None):
        try:
            sql = f"DELETE FROM {self.table} WHERE {where_clause}"
            self.cursor.execute(sql, params or {})
            self.conn.commit()
            return True, "Deleted Successfully", None
        
        except Exception as e:
            # print(f"An error occurred during delete operation: {e}")
            return False, f"An error occurred during delete operation: {e} from {__name__}", None

    def close_connection(self):
        try:
            self.conn.close()
        except Exception as e:
            print(f"An error occurred while closing the connection: {e} from {__name__}")
