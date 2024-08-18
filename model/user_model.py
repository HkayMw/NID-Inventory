# model/user_model.py

from model.model import Model
from datetime import datetime

class UserModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.table = 'user'


