from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.clock import Clock
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout
from controller.sync_controller import SyncController
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

# Builder.load_file('view/UI.kv')
import os
import sys
import shutil
from pathlib import Path
import time


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('sync_view.kv'))
# Builder.load_file('view/user_profile/user_profile_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/user_profile/user_profile_view.kv')



class SyncScreen(Screen):
    def __init__(self, **kwargs):
        super(SyncScreen, self).__init__(**kwargs)
        self.sync_controller = SyncController()
        self.app = MDApp.get_running_app()
        self.notice = self.app.root.ids.notice
        self.pending_sync = None
        self.count = self.ids.pending_records_count
        self.progress_total = 0
        self.progress_current = 0
        self.api_dialog = None
        
        # self.api_path = resource_path('')
        
        
    def on_enter(self, *args):
        # self.ids.current_password.text = ''
        # self.ids.new_password.text = ''
        # self.ids.new_password1.text = ''
        self.notice.text = ''
        self.count.text = ''
        self.progress_total = 0
        self.progress_current = 0
        
        pass
    
    def on_kv_post(self, base_widget):
        # Bind to the text property of the label
        self.ids.pending_records_count.bind(text=self.on_count_change)
    
    
    def on_count_change(self, instance, value):
        self.update_progress_bar() 
        

    def check_pending_records(self):
        # check for records pending syncing
        self.notice.text = ''
        self.progress_total = 0
        self.progress_current = 0
        # current_url = self.read_api_url()
        # if current_url:
        #     print(f"Current API URL: {current_url}")
        
        # new_url = "http://192.168.137.1/id_availability_portal/api/upload.php"
        # self.write_api_url(new_url)
        
        # print('checking pending')
        
        success, message, data = self.sync_controller.check_pending_records()
        if success:
            self.pending_sync = data
            if not data:
                self.count.text = '0'
                self.progress_current = 0
                self.update_progress_bar()
                self.notice.text = 'There are no pending records.'
                return
            self.progress_total = len(data)
            self.count.text = str(len(data))
            
            
        else:
            self.pending_sync = None
            
            self.notice.text = 'Something went wrong, contact admin'
            
            
        
    
    def start_sync(self):
        # initialize syncing
        self.notice.text = ''
        # self.
        
        print('Syncing...')
        
        self.check_pending_records()
        url = self.read_api_url()
        
        pending = self.pending_sync 
        if not pending:
            self.count.text = '0'
            self.progress_current = 0
            self.update_progress_bar()
            self.notice.text = 'There are no pending records.'
            return
        
        # Start syncing each record with a delay between each to allow UI updates
        self.progress_current = 0
        Clock.schedule_once(lambda dt: self.sync_next_record(url), 0)

    def sync_next_record(self, url):
        """Sync the next record in self.pending_sync."""
        if not self.pending_sync or self.progress_current >= self.progress_total:
            self.pending_sync = None
            self.notice.text = 'Syncing complete.' if self.progress_total else 'Something went wrong, contact admin.'
            return

        record = self.pending_sync[self.progress_current]
        signature, id_number, status = record[:3]
        availability = 'Collected' if status == 'Issued' else status

        data = {
            "id_number": id_number,
            "availability_status": availability
        }

        success, message, response = self.sync_controller.sync_to_client_portal(data, url)
        if success:
            print(self.sync_controller.update_client_portal(signature))

        # Update progress bar and pending records count
        self.progress_current += 1
        self.count.text = str(int(self.count.text) - 1)
        self.update_progress_bar()

        # Schedule the next sync attempt with a slight delay for UI responsiveness
        Clock.schedule_once(lambda dt: self.sync_next_record(url), 0.5)

    def update_progress_bar(self):
        count_value = self.progress_current
        try:
            
            progress_percentage = (count_value / self.progress_total) * 100
        except Exception as e:
            progress_percentage = 0.1
        self.ids.syncing_progress_bar.value = progress_percentage
    
    
    
    def open_api_dialog(self):
        self.api_dialog = None
        # Retrieve current API URL
        current_url = self.read_api_url() or "No URL set"
        
        # Create the input field with the current URL as initial text
        if not self.api_dialog:
            self.api_input = MDTextField(
                hint_text="API URL",
                text=current_url,  # Show current URL in the input field
                mode="rectangle",
                icon_left='link',
            )

            # Layout to show the current URL above the input field
            content_layout = MDBoxLayout(orientation="vertical", size_hint_y=None)
            # content_layout.bind(minimum_height=content_layout.setter('height'))  # Allow height to adjust based on content
            content_layout.add_widget(MDLabel(text=f"Current URL: {current_url}", size_hint_y=None, height=dp(30), color = self.app.theme_cls.primary_color, padding = [20]))
            content_layout.add_widget(self.api_input)

            self.api_dialog = MDDialog(
                title="Configure API",
                size_hint=(None, None),
                size=(dp(500), dp(480)),
                type="custom",
                content_cls=content_layout,
                buttons=[
                    MDFlatButton(
                        text="Cancel", on_release=lambda x: self.api_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="Add",
                        on_release=lambda x: self.save_api_url()
                    ),
                ],
            )

        self.api_dialog.open()

    def save_api_url(self):
        # Get the new URL from the input field and save it
        new_url = self.api_input.text.strip()
        if new_url:
            self.write_api_url(new_url)
            self.api_dialog.dismiss()
            print(f"New API URL saved: {new_url}")
        else:
            print("No URL provided.")
    
    # Define the path to your text file
    def get_api_path(self):
        # Get the user's home directory
        home_directory = Path.home()
        # Define the path for your application's api
        api_path = home_directory / "IDInventoryManager" / "client_portal.txt"
        
        # Ensure the directory exists
        os.makedirs(api_path.parent, exist_ok=True)

        return str(api_path)

    def read_api_url(self):
        """Reads the API URL from the client_portal.txt file."""
        
        file_path = self.get_api_path()
        if not Path(file_path).exists():
            self.notice.text = 'API is not set yet,'
            return
        
        try:
            with open(file_path, 'r') as file:
                api_url = file.readline().strip()
                return api_url
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def write_api_url(self,api_url):
        """Writes the provided API URL to the client_portal.txt file."""
        
        file_path = self.get_api_path()
        
        try:
            with open(file_path, 'w') as file:
                file.write(api_url.strip() + '\n')
                print(f"API URL has been updated to: {api_url}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Usage
    # Read the current API URL
# key = SyncScreen()
# current_url = key.read_api_url()
# if current_url:
#     print(f"Current API URL: {current_url}")

# # Update the API URL
# new_url = "http://192.168.137.1/id_availability_portal/api/upload.php"
# key.write_api_url(new_url)

