# model/storage_unit_model.py

from model.model import Model

class StorageUnitModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.table = 'storage_unit'


