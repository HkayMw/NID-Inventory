# controller/id_controller.py

from controller.controller import Controller
from model.id_model import IdModel




class IdController(Controller):
    def __init__(self):
        super().__init__(IdModel())
        
    def add_id(self,data):
        
        success, message = self.model.create(data)
        
        if success:
            record_id = message
            return success, f"Record Added Successfully: "
        else:
            return False, message