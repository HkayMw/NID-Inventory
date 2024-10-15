# model/user_model.py

from model.model import Model

class batchModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.table = 'batch'


