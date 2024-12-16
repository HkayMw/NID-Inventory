from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout

from controller.sms_controller import SMSController
from controller.id_controller import IdController

# Builder.load_file('view/UI.kv')
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('notify_view.kv'))
# Builder.load_file('view/admin/notifyClient/notify_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/admin/notifyClient/notify_view.kv')



class NotifyScreen(Screen):
    def __init__(self, **kwargs):
        super(NotifyScreen, self).__init__(**kwargs)
        self.sms_controller = SMSController()
        self.id_controller = IdController()
        self.app = MDApp.get_running_app()
        self.notice = self.app.root.ids.notice
        


    def on_enter(self, *args):
        self.load_to_be_notified()
        self.sms_controller.init_api()
        return super().on_enter(*args)
    
    def load_to_be_notified(self):
        success, message, pending = self.sms_controller.get_to_be_notified()
        if success:
            self.ids.pending_notices.text = str(pending[0][0])
        else:
            print("something went wrong loading pending")
    
    def send_sms(self):
        sms = self.ids.sms_body.text
        limit = self.ids.sms_limit.text
        
        if not sms:
            return
        
        if len(sms) >= 160:
            self.notice.color = self.app.theme_cls.error_color
            
            self.notice.text = 'Message is limited to 160 charaters only'
            return
        
            
        success, message, notified = self.sms_controller.send_sms(sms, limit)
        if success:
            # self.ids.pending_notices.text = str(pending[0][0])
            print(notified)
            
            success, not_updated, updated = self.id_controller.update_notified_id(notified)
            if success:
                self.load_to_be_notified()
                self.notice.color = [0, 1, 0, 1]
                self.notice.text = f'{updated} Clients notified successfully'
        
        else:
            self.notice.color = self.app.theme_cls.error_color

            self.notice.text = message   
        # sms_data = {'sms': sms, 'limit': limit}
        
        
        # print(f'SMS: {sms}\nLimit: {limit}')
        # pass