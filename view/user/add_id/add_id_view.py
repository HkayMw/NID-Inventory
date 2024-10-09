from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from controller.id_controller import IdController
from controller.batch_controller import BatchController
# from controller.sorting import IdController
from Assets.qr_code import QRCode
from datetime import date, datetime
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
# from kivy.metrics import dp
# from model.current_user import CurrentUser
# from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
# import sqlite3
# from kivymd.uix.pickers import MDDatePicker
# from kivymd.uix.pickers import MDDockedDatePicker

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/add_id/add_id_view.kv')


class AddIDScreen(Screen):
    def __init__(self, **kwargs):
        super(AddIDScreen, self).__init__(**kwargs)
        self.id_controller = IdController()
        self.batch_controller = BatchController()
        self.app = MDApp.get_running_app()
        # Clear notice
        self.notice = self.app.root.ids.notice
        self.progress = self.app.root.ids.progress
        
        
        
    
    def on_enter(self, *args):
        # Set focus on the MDTextField after the screen has entered
        self.ids.qr_code.focus = True
        self.set_batch_name() 
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        # print("user_id: ", self.user_id)
         
        # self.ids.count.text = str(len(self.app.current_batch['ids']))    
        
        # Update count and progress bar
        self.ids.count.text = str(len(self.app.current_batch['ids']))
        # self.update_progress_bar()  # Update progress bar based on the current count

    def on_kv_post(self, base_widget):
        # Bind to the text property of the label
        self.ids.count.bind(text=self.on_count_change)

    def on_count_change(self, instance, value):
        self.update_progress_bar()  # Update progress bar when count changes

    def update_progress_bar(self):
        try:
            count_value = int(self.ids.count.text)
            # print("Count: ", count_value)
        except ValueError:
            count_value = 0  # Default to 0 if the text is not a valid integer
        progress_percentage = (count_value / 50) * 100
        self.ids.progress_bar.value = progress_percentage + .1
        # print("Progress: ", self.ids.progress_bar.value)
        
        
    def assign_batch_name(self):    
        # get batch name
        batch_name = self.ids.batch_name.text
        
        # keep batch name
        self.app.current_batch['batch_name'] = batch_name
        # print(batch_name)
        # print(self.app.current_batch['batch_name'])
        
    def show_reset_dialog(self):
        if not hasattr(self, 'reset_dialog'):
            self.reset_dialog = MDDialog(
                title="Confirm Reset",
                text="Are you sure you want to reset?, all IDs scanned this session will not be added to database",
                size_hint=(0.4, 0.2),
                buttons=[
                    MDRaisedButton(
                        text="Cancel",
                        on_release=self.close_reset_dialog
                    ),
                    MDRaisedButton(
                        text="Reset",
                        on_release=self.reset
                    )
                ]
            )
        self.reset_dialog.open()
        
    def close_reset_dialog(self, instance):
        self.reset_dialog.dismiss()
        
    # todo: fix progress bar on reset
    def reset(self, instance):
        self.app.current_batch = {"batch_name": '', "ids": []}
        self.ids.count.text = str(len(self.app.current_batch['ids']))
        self.ids.progress_bar.value = (int(self.ids.count.text)/50)*100
        self.update_progress_bar()  # Update progress bar on reset
        self.close_reset_dialog(instance)
        
        
    def refocus_qr_code(self, *args):
        # Set focus back to the MDTextField after the delay
        self.ids.qr_code.focus = True    
        
    def add_id(self):
        
        current_batch = self.app.current_batch
        
        # Clear notice
        notice = self.notice.text
        notice = ''
        # self.progress.active = True
        
        # Process ID QR Code
        qr_code = self.ids.qr_code.text
        qr_code = QRCode(qr_code.upper())
        success, message, id = qr_code.process()
        
        if success:
            # Go on ONLY if count is not maxed out (count < 50)
            count = int(self.ids.count.text)
            if count < 50:
            
                # Go on ONLY if it is a valid ID QR Code
                if id['type'] == "03":
                    
                    # Go on ONLY if id is new in current batch
                    current_ids = current_batch["ids"]
                    all_clear = True
                    
                    if len(current_ids):
                        for idx in current_ids:
                            if idx["signature"] == id["signature"]:
                                all_clear = False
                        
                    if not all_clear:
                        
                        # todo: make notice error color
                        notice ="ID already added in the current batch"
                        self.ids.qr_code.text = ''
                        Clock.schedule_once(self.refocus_qr_code, 0.1)
                    else:
                        
                        # Go on ONLY if id is new in current database
                        success, message, idx = self.id_controller.search_id("signature", signature = id['signature'])
                        if success and idx:
                            # ID exists in db
                            
                            # todo: make notice error color
                            notice = "ID already exists in database"
                            self.ids.qr_code.text = ''
                            Clock.schedule_once(self.refocus_qr_code, 0.1)
                        else:
                            # ID is new in db
                        
                            #Remove QR Type fro id record
                            del id['type']
                            
                            status = "Available"
                            created_on = str(datetime.now())
                            created_by = self.user_id
                            
                            #Append all data to be added
                            id = {**id, "status": status, "created_on": created_on, "created_by": created_by}
                            
                            current_batch['ids'].append(id)
                            self.ids.count.text = str(len(current_batch['ids']))
                            
                            self.ids.qr_code.text = ''
                            Clock.schedule_once(self.refocus_qr_code, 0.1)
                          
                else:
                    notice = 'Only National ID QR code allowed here'
                    # Clear Qr Code field
                    self.ids.qr_code.text = ''
                    Clock.schedule_once(self.refocus_qr_code, 0.1)
                    
            else:
                notice = 'Batch size has reached acceptable maximum'
                self.ids.qr_code.text = ''
                
        else:
            notice = message
            # print(message)
            # Clear Qr Code field
            self.ids.qr_code.text = ''
            Clock.schedule_once(self.refocus_qr_code, 0.1)
            
            
                
        self.notice.text = notice
        
        
    def set_batch_name(self):
        today = date.today()

        # Accessing attributes
        year = today.year
        month = today.month
        day = today.day
        
        today_date = datetime(year, month, day)

        # Format the month as a word
        batch_prefix = today_date.strftime("%B%Y")
        
        #get batch number
        success, message, result = self.batch_controller.get_batch(batch_prefix)
        
        if success:
            batch_number = len(result) + 1
            self.ids.batch_name.text = f'{batch_prefix}_{batch_number}'
            # print(batch_prefix, " ", result)
            
        
        # print(success, " ", message, " ", result)
        # print(self.batch_controller.get_batch_number(batch_prefix))
        
        # self.ids.batch_prefix.text = today_date.strftime("%B%y") + "_"
    
