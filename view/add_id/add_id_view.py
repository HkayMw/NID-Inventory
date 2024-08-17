from kivy.uix.screenmanager import Screen
from controller.id_controller import IdController
from Assets.qr_code import QRCode
import datetime
from model.current_user import CurrentUser
from kivy.lang import Builder
import sqlite3

# Builder.load_file('view/UI.kv')
Builder.load_file('view/add_id/add_id_view.kv')


class AddIDScreen(Screen):
    def __init__(self, **kwargs):
        super(AddIDScreen, self).__init__(**kwargs)
        self.controller = IdController()
        
    def add_id(self):
        
        # Process ID QR Code
        qr_code = self.ids.qr_code.text
        self.qr_code = QRCode(qr_code.upper())
        id = self.qr_code.process()
        
        # ONLY Run if it is a valid ID QR Code
        if id['type'] == "03":
            
            #Rem QR Type fro id record
            del id['type']
            # print(self.controller.add_id(*args))
            current_user = CurrentUser()
            user_id = current_user.get_user_details()['id_number']
            
            issue_date = self.ids.issue_date.text
            status = "AVAILABLE"
            created_on = str(datetime.datetime.now())
            created_by = user_id
            sorting_key= id["sorting_key"]
            
            #Append all data to be added
            id_record = {**id, "status": status, "issue_date": issue_date, "created_on": created_on, "created_by": created_by, "sorting_key": sorting_key}
        
            #Add id_record
            try:
                status, message = self.controller.add_id(id_record)
                # print(self.controller.add_id(id_record))
                if status == None:
                    self.ids.status.text = F"{message}"
                    
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                    
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: id_record.id_number, id_record.issue_date" in str(e):
                    self.ids.status.text = f"A record with the specified ID # and issue date already exists in the database."
                    
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                    
                else:
                    # Re-raise the exception if it's a different IntegrityError
                    raise
            
                # self.ids.qr_code.focus = True
                

        # print(id_record)
        
        # self.ids.qr_code.text = ''
        
        
    
