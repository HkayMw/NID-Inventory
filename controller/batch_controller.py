# controller/batch_controller.py

from kivymd.app import MDApp
from controller.controller import Controller
from model.batch_model import batchModel
# from model.current_user import CurrentUser
from datetime import date, datetime

class BatchController(Controller):
    def __init__(self):
        super().__init__(batchModel())
        self.app = MDApp.get_running_app()
        # self.current_user = self.app.user_details
        # self.user_id = self.current_user['id_number']

    def get_batch(self, batch_prefix=None, id=None):
        
        if id:
            where_clause = 'id = :id'
            params = {'id': id}
            
            success, message, result = self.read(where_clause, params)
        
            if success:
                batch = {'id': result[0][0], 'name': result[0][1], 'storage': result[0][2], 'count': result[0][3], 'qr_text': result[0][4], 'created_on': result[0][5], 'updated_on': result[0][6], 'created_by': result[0][7], 'updated_by': result[0][8], }
                
                return success, message, batch
            else:
                return success, message, None
            
        
        where_clause = 'name LIKE :name'
        params = {'name': f'{batch_prefix}%'}
        
        success, message, result = self.read(where_clause, params)
        
        if success:
            return success, f"{batch_prefix}", result
        else:
            return success, message, None
        
    def add_batch(self, batch_name, count, storage, qr_text, user_id):
        
        #check if batch already exists
        success, message, row = self.get_batch(batch_prefix=batch_name)
        if success:
            if len(row) > 0:
                # count = int(row[3]) + count
                
                # where_clause = 'name = :name'
                # params = {'name': batch_name}
                # count = {"count": count}
            
                # success, message, id = self.update(count, where_clause, params)
                
                return False, "Batch Already added", None
                
            else:
                name = batch_name
                # count = 1
                # qr_text = "Batch Name: " + batch_name
                created_on = str(datetime.now())
                created_by = user_id
                
                batch = {"name": name, "count": count, "storage": storage, "created_on": created_on, "created_by": created_by, "qr_text": qr_text}
                
        
                success, message, id = self.create(batch)
                return success, message, id
                
        