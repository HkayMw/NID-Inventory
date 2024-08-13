# controller/users_controller.py

from controller.controller import Controller
from model.users_model import UsersModel

class UsersController(Controller):
    def __init__(self):
        super().__init__(UsersModel())

    def validate_user(self, id_no, password):
        user = self.model.validate_user(id_no, password)
        # return print(id_no + password)
        if user:
            return True, "Login Successful"
        else:
            return False, "Wrong credentials"

    def add_user(self):
        pass
