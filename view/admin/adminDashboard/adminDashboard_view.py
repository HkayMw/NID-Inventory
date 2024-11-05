
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp

from controller.id_controller import IdController
from controller.dashboard_controller import DashboardController

import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Builder.load_file('view/admin/adminDashboard/adminDashboard_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/admin/adminDashboard/adminDashboard_view.kv')

Builder.load_file(resource_path('adminDashboard_view.kv'))

class AdminDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminDashboardScreen, self).__init__(**kwargs)
        
        self.app = MDApp.get_running_app()
        self.id_controller = IdController()
        self.dashboard_controller = DashboardController()
        
        self.notice = self.app.root.ids.notice
        
    def on_enter(self, *args):
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        
        self.ids.ids_added.text = ''
        self.ids.ids_issued.text = ''
        self.ids.ids_in_inventory.text = ''
        self.ids.storage_units.text = ''
        self.ids.users.text = ''
        self.ids.sms.text = ''
        self.load_dashboard('Day')
        
    def load_dashboard(self, period):
        
        # print(period)
        success, message, data = self.dashboard_controller.load_dashboard(period)
        
        # print(f'success: {success} message: {message}\ndata: {data}')
        
        if success:
            self.ids.ids_added.text = f"{data['added_ids']}"
            self.ids.ids_issued.text = f"{data['issued_ids']}"
            self.ids.ids_in_inventory.text = f"{data['total_ids']}"
            self.ids.storage_units.text = f"{data['storage_units']}"
            self.ids.users.text = f"{data['users']}"
            self.ids.sms.text = f"{data['sent_sms']}"
        else:
            self.notice.text = "Something went wrong while loading dashboard data"
        