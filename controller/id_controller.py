# controller/id_controller.py

from controller.controller import Controller
from model.id_model import IdModel




class IdController(Controller):
    def __init__(self):
        super().__init__(IdModel())
        
    def add_id(self,data):
        
        return self.model.create(data), "Record Added Successfully"