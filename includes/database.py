import sqlite3

conn = sqlite3.connect('id_inventory.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               first_name TEXT,
               last_name TEXT,
               other_names TEXT,
               created_on DATETIME,
               updated_on DATETIME)''')

