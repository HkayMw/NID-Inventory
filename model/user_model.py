# model/user_model.py

from model.model import Model
from datetime import datetime
import hashlib

class UserModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.table = 'user'

    def validate_user(self, id_number, password):
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Fetch the user with the provided id_no and hashed password
        # return self.fetch_one('SELECT * FROM user WHERE id_number=? AND password_hash=?', id_no, password_hash)
        where_clause = 'id_number = :id_number AND password_hash = :password_hash'
        params = {'id_number': id_number, 'password_hash': password_hash}
        return self.read(where_clause, params)

    def add_user(self, id_no, first_name, last_name, other_names, password_hash, user_type, created_by):
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
            INSERT INTO user (
                id_number, 
                firstname, 
                lastname, 
                othernames, 
                password_hash, 
                user_type, 
                created_on, 
                created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.execute_query(query, id_no, first_name, last_name, other_names, password_hash, user_type, created_on, created_by)
        return (f"User {id_no} added successfully!")
