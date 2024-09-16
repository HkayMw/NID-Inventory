# controller/users_controller.py

from controller.controller import Controller
from model.user_model import UserModel
import hashlib


class UserController(Controller):
    def __init__(self):
        super().__init__(UserModel())

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

    def add_user(self):
        pass
