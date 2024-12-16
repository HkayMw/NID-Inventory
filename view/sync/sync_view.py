from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.clock import Clock
from controller.sync_controller import SyncController
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import os
import requests
import sys
import shutil
from pathlib import Path
import time
import threading  # Import threading for background tasks

# Function to get the absolute path for resources (for PyInstaller compatibility)
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('sync_view.kv'))

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
        
    def on_enter(self, *args):
        self.notice.text = ''
        self.count.text = ''
        self.progress_total = 0
        self.progress_current = 0
        
        # items = self.app.root.ids.side_nav.get_screen('admin_nav').ids.navigation_rail.children[0].children[0].children
        # for item in items:
        #     item.active = False
            
        # items = self.app.root.ids.side_nav.get_screen('clerk_nav').ids.navigation_rail.children[0].children[0].children
        # for item in items:
        #     item.active = False 
    
    def on_kv_post(self, base_widget):
        self.ids.pending_records_count.bind(text=self.on_count_change)
    
    def on_count_change(self, instance, value):
        self.update_progress_bar() 
        
    def check_pending_records(self):
        success, message, data = self.sync_controller.check_pending_records()
        if success:
            self.pending_sync = data
            self.progress_total = len(data) if data else 0
            self.count.text = str(len(data)) if data else '0'
            if not data:
                self.notice.color = self.app.theme_cls.primary_color
                self.notice.text = 'There are no pending records.'
                return
        else:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = 'Something went wrong, contact admin'
            return
    
    def check_api_connection(self):
        pending = id(self.ids.pending_records_count)
        if not pending:
            return
        
        """Checks if the API is reachable."""
        url = self.read_api_url()
        if not url:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = 'API URL is not set. Please configure it.'
            return

        try:
            # Send a GET request to the API URL to check connectivity
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # return
                pass
            else:
                self.notice.color = self.app.theme_cls.error_color
                self.notice.text = 'Failed to connect to the API. Status code: ' + str(response.status_code)
                return
        except requests.ConnectionError:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = 'Unable to connect to the API. Check your internet connection or the API URL.'
            return
        except Exception as e:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = f"An error occurred: {e}"
            return

    def start_sync(self):
        self.check_pending_records()
        threading.Thread(target=self.check_api_connection).start()
        
        """Start syncing process only if API is reachable."""
        # if not self.check_api_connection():
        #     # If the connection check fails, stop here
        #     return
        
        # Run the sync process in a separate thread if the API connection is successful
        threading.Thread(target=self.sync_in_background).start()

    def sync_in_background(self):
        """Starts syncing in the background to keep the UI responsive."""
        url = self.read_api_url()
        
        if not self.pending_sync:
            Clock.schedule_once(lambda dt: self.update_no_pending_message(), 0)
            return
        
        # Start syncing each record without blocking the main thread
        self.progress_current = 0
        self.sync_records(url)

    def sync_records(self, url):
        """Sync records one by one."""
        for record in self.pending_sync:
            if not self.pending_sync or self.progress_current >= self.progress_total:
                break
            # Sync a single record
            self.sync_record(record, url)
            # Update UI on the main thread
            Clock.schedule_once(lambda dt: self.update_ui_after_sync(), 0.5)
        
        # Final UI update after syncing completes
        Clock.schedule_once(lambda dt: self.finish_sync(), 0)

    def sync_record(self, record, url):
        signature, id_number, status = record[:3]
        availability = 'Collected' if status == 'Issued' else status
        data = {"id_number": id_number, "availability_status": availability}

        success, message, response = self.sync_controller.sync_to_client_portal(data, url)
        if success:
            print(self.sync_controller.update_client_portal(signature))
        self.progress_current += 1

    def update_ui_after_sync(self):
        """Update the progress and count labels."""
        self.count.text = str(int(self.count.text) - 1)
        self.update_progress_bar()

    def finish_sync(self):
        self.notice.color = [0, 1, 0, 1]  if self.progress_total else self.app.theme_cls.primary_color
        self.notice.text = 'Syncing complete.' if self.progress_total else 'No records to sync.'

    def update_no_pending_message(self):
        self.notice.color = self.app.theme_cls.primary_color
        self.notice.text = 'There are no pending records.'
        self.count.text = '0'
        self.update_progress_bar()

    def update_progress_bar(self):
        try:
            progress_percentage = (self.progress_current / self.progress_total) * 100
        except ZeroDivisionError:
            progress_percentage = 0
        self.ids.syncing_progress_bar.value = progress_percentage

    # Additional methods for API URL management (unchanged)
    # ... (open_api_dialog, save_api_url, get_api_path, read_api_url, write_api_url)

    
    
    
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
            content_layout = MDBoxLayout(orientation="vertical", size_hint_y=None, height = dp(120))
            # content_layout.bind(minimum_height=content_layout.setter('height'))  # Allow height to adjust based on content
            content_layout.add_widget(MDLabel(text=f"Current URL: {current_url}", size_hint_y=None, height=dp(70), color = self.app.theme_cls.primary_color, padding = [20]))
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
            self.notice.color = self.app.theme_cls.error_color  
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
                # print(f"API URL has been updated to: {api_url}")
                self.notice.color = [0, 1, 0, 1] 
                self.notice.text = f"API updated to: {api_url}"
        except Exception as e:
            self.notice.color = self.app.theme_cls.error_color  
            # print(f"An error occurred: {e}")
            self.notice.text = "Error while setting API, contact admin"

    # Usage
    # Read the current API URL
# key = SyncScreen()
# current_url = key.read_api_url()
# if current_url:
#     print(f"Current API URL: {current_url}")

# # Update the API URL
# new_url = "http://192.168.137.1/id_availability_portal/api/upload.php"
# key.write_api_url(new_url)

