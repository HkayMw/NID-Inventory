from kivy.uix.screenmanager import Screen
from controller.id_controller import IdController
# from controller.sorting import IdController
from Assets.qr_code import QRCode
import datetime
from model.current_user import CurrentUser
from kivy.uix.boxlayout import BoxLayout
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
        qr_code = QRCode(qr_code.upper())
        success, message, id = qr_code.process()
        
        # ONLY Run if it is a valid ID QR Code
        if id['type'] == "03":
            # print(id)
            
            #Rem QR Type fro id record
            del id['type']
            # print(self.controller.add_id(*args))
            current_user = CurrentUser()
            user_id = current_user.get_user_details()['id_number']
            
            issue_date = self.ids.issue_date.text
            status = "AVAILABLE"
            created_on = str(datetime.datetime.now())
            created_by = user_id
            # sorting_key= id["sorting_key"]
            
            #Append all data to be added
            id_record = {**id, "status": status, "issue_date": issue_date, "created_on": created_on, "created_by": created_by}
        
            #Add id_record
            try:
                success, message, record_id = self.controller.add_id(id_record)
                # print(self.controller.add_id(id_record))
                if success:
                    self.ids.status.text = F"{message} {id_record['id_number']}"
                    
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                    self.ids.qr_code.focus = True
                    
                elif message == "An error occurred: UNIQUE constraint failed: id_record.id_number, id_record.issue_date":
                    self.ids.status.text = f"A record with ID Number: {id_record['id_number']} and issue date: {id_record['issue_date']} already exists in the database."
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                else:
                    print(message)
            except Exception as e:
            # print(f"An unexpected error occurred: {e}")    
                self.ids.status.text = f"An unexpected error occurred: {e}"
            
                

        # print(id_record)
        
        # self.ids.qr_code.text = ''
        
        
    
