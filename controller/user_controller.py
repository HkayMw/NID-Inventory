# controller/users_controller.py

from controller.controller import Controller
from model.user_model import UserModel

class UserController(Controller):
    def __init__(self):
        super().__init__(UserModel())

    def validate_user(self, id_no, password):
        user = self.model.validate_user(id_no, password)
        # return print(id_no + password)
        if user:
            return True, "Login Successful", user
        else:
            return False, "Wrong credentials", None

    def add_user(self):
        pass
