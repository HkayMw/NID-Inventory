# controller/users_controller.py

from kivymd.app import MDApp
from controller.controller import Controller
from model.user_model import UserModel
from datetime import datetime
import hashlib


class UserController(Controller):
    def __init__(self):
        super().__init__(UserModel())
        self.app = MDApp.get_running_app()

    def validate_user(self, id_number, password):
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Fetch the user with the provided id_no and hashed password
        where_clause = 'id_number = :id_number AND password_hash = :password_hash'
        params = {'id_number': id_number, 'password_hash': password_hash}
        success, message, user = self.read(where_clause, params)
        
        if success:
            # user = message
            if user:
                return success, "Login Successful", user[0]
            else:
                return False, "Wrong credentials", None
        else:
            return False, message, None

    def add_user(self, user_data):
        
        created_by = self.app.user_details['id_number']
        created_on = str(datetime.now())
        password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
        
        del user_data['password']
        
        user_data = {**user_data, 'password_hash': password_hash, 'created_by': created_by, 'created_on': created_on}
        
        
        success, message, last_row_id = self.create(user_data)
        
        if success:
            return success, message, user_data['id_number']
        else:
            return False, message, None
        
    def update_user(self, user_data):
        updated_by = self.app.user_details['id_number']
        updated_on = str(datetime.now())
        
        if user_data['password']:
            password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
            
            
            user_data = {**user_data, 'password_hash': password_hash, 'updated_by': updated_by, 'updated_on': updated_on}
        else:
            user_data = {**user_data, 'updated_by': updated_by, 'updated_on': updated_on} 
        
        del user_data['password']
        
        where_clause = 'id_number = :id_number'
        params = {'id_number': user_data['id_number']}
           
        success, message, last_row_id = self.update(user_data, where_clause, params)
        if success:
            return success, message, user_data['id_number']
        else:
            return False, message, None
        
    
    def remove_user(self, id_number):
        
        where_clause = 'id_number = :id_number'
        params = {'id_number': id_number}
        
        success, message, user = self.delete(where_clause, params)
        if success:
            return success, message, id_number
        else:
            return False, message, None
        
        
    
    def search_user(self, user_data=None):
        
        if user_data:
            id_number = user_data['id_number']
            firstname = user_data['firstname']
            lastname = user_data['surname']
            
            if id_number:
                where_clause = 'id_number = :id_number'
                params = {'id_number': id_number}
            elif firstname and lastname:
                where_clause = 'firstname LIKE :firstname and lastname LIKE :lastname'
                params = {'firstname': f'%{firstname}%', 'lastname': f'%{lastname}%'}
            elif firstname:
                where_clause = 'firstname LIKE :firstname'
                params = {'firstname': f'%{firstname}%'}
            elif lastname:
                where_clause = 'lastname LIKE :lastname'
                params = {'lastname': f'%{lastname}%'}
                
            # print(where_clause)
            # print(params)
            
            success, message, rows = self.read(where_clause, params)
            if success:
                if rows:
                    columns = ['id_number', 'firstname', 'surname', 'othernames', 'password_hash', 'user_type', 'created_on', 'updated_on', 'created_by', 'updated_by']
                    
                    users = [dict(zip(columns, row)) for row in rows]
                    
                    return success, message, users
                else:
                    return success, message, None
            else:
                return False, message, None
        else:
            # query = 'SELECT * FROM user ORDER BY CASE WHEN updated_on IS NOT NULL THEN 0 ELSE 1 END, updated_on DESC, created_on DESC;'
            
            query = '''
                SELECT * FROM user 
                    ORDER BY 
                        CASE 
                            WHEN updated_on IS NOT NULL AND updated_on > created_on THEN updated_on 
                            ELSE created_on 
                        END DESC;'''
            success, message, rows = self.custom_query(query)
            if success:
                columns = ['id_number', 'firstname', 'surname', 'othernames', 'password_hash', 'user_type', 'created_on', 'updated_on', 'created_by', 'updated_by']
                
                users = [dict(zip(columns, row)) for row in rows]
                
                return success, message, users
            else:
                return False, message, None
        
