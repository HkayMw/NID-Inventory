from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.id_controller import IdController
# from controller.sorting import IdController
from Assets.qr_code import QRCode
import datetime
from kivy.metrics import dp
from model.current_user import CurrentUser
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import sqlite3
from kivymd.uix.pickers import MDDatePicker
# from kivymd.uix.pickers import MDDockedDatePicker

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/add_id/add_id_view.kv')


class AddIDScreen(Screen):
    def __init__(self, **kwargs):
        super(AddIDScreen, self).__init__(**kwargs)
        self.controller = IdController()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        self.progress = self.app.root.ids.progress
        # self.notice.text = ''
        
############################### Date Picker Methods Start #############################################
        
    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        # date_dialog = MDDatePicker()
        # date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        # date_dialog.open()
        
        date_dialog = MDDatePicker()
        date_dialog.open()
        
############################### Date Picker Methods End #############################################
        
        
    def add_id(self):
        
        # Clear notice
        notice = self.notice.text
        notice = ''
        self.progress.active = True
        
        # Process ID QR Code
        qr_code = self.ids.qr_code.text
        qr_code = QRCode(qr_code.upper())
        success, message, id = qr_code.process()
        
        if success:
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
                
                #Append all data to be added
                id_record = {**id, "status": status, "issue_date": issue_date, "created_on": created_on, "created_by": created_by}
            
                #Add id_record
                try:
                    success, message, record_id = self.controller.add_id(id_record)
                    # print(self.controller.add_id(id_record))
                    if success:
                        notice = F"{message} {id_record['id_number']}"
                        
                        # Clear Qr Code field
                        self.ids.qr_code.text = ''
                        self.ids.qr_code.focus = True
                        
                    elif message == "An error occurred: UNIQUE constraint failed: id_record.id_number, id_record.issue_date":
                        notice = f"A record with ID Number: {id_record['id_number']} and issue date: {id_record['issue_date']} already exists in the database."
                        # Clear Qr Code field
                        self.ids.qr_code.text = ''
                        
                    else:
                        notice = message
                        # Clear Qr Code field
                        self.ids.qr_code.text = ''
                        
                except Exception as e:
                # print(f"An unexpected error occurred: {e}")    
                    notice = f"An unexpected error occurred: {e}"
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                    
            else:
                notice = 'Only National ID QR code allowed here'
                # Clear Qr Code field
                self.ids.qr_code.text = ''
                
        else:
            notice = message
            print(message)
            # Clear Qr Code field
            self.ids.qr_code.text = ''
            
                
        self.notice.text = notice
        self.progress.active = False
        
        # print(id_record)
        
        # self.ids.qr_code.text = ''
        
    def show_date_picker(self):
        date_dialog = MDDatePicker(
            title="Select Month and Year",
            selector="month",  # This allows only month and year selection
            min_year=2000,  # Optionally set minimum year
            max_year=2030,  # Optionally set maximum year
        )
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        # Extract month and year from the selected value
        print(f"Selected Date: {value.strftime('%B %Y')}")   
    
