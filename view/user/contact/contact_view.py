from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.clock import Clock
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
import csv
import os

from Assets.qr_code import QRCode
from controller.contact_controller import ContactController

# Builder.load_file('view/UI.kv')
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('contact_view.kv'))
# Builder.load_file('view/user/contact/contact_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/user/contact/contact_view.kv')



class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        # self.controller = UserController()
        self.data_tables = None
        self.contact_controller = ContactController()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        # self.notice.text = ''
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=['.csv']  # Restrict to CSV files
        )
        
        self.contacts = []
        self.invalid_contact_input = []
        self.path = None
        Clock.schedule_once(self.initialize_table, 0.2)

    def on_enter(self, *args):
        # print(self.parent.current)
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        self.validation_event = None
        
    def on_leave(self, *args):
        self.ids.id_number_field.text = ''
        self.ids.phone_number_field.text = ''
        self.ids.qr_code.text = ''
        self.ids.id_number_field1.text = ''
        return super().on_leave(*args)
        
    def initialize_table(self, *args):
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            
            use_pagination=True,

            # check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("ID Number", dp(40)),
                ("Phone Number", dp(40)),
            ],
            row_data=[]
        )
       
        # self.ids.lastname_field.text = "something"
        self.ids.table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.table_container.add_widget(layout)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        
        
    def open_file_manager(self):
        self.notice.text = ''
        # Get the Documents folder path
        if platform == 'win':
            documents_folder = os.path.join(os.environ['USERPROFILE'], 'Documents')
        elif platform == 'linux' or platform == 'macosx':
            documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')

        # Open the file manager at the Documents folder
        self.file_manager.show(documents_folder)

    def select_path(self, path):
        '''This function will be called when a file is selected.'''
        self.exit_manager()
        self.ids.file_name.text = f"{os.path.basename(path)}"
        # self.notice.text= f"Selected file: {path}"
        self.path = path

        # Call a function to process the CSV file
        # self.process_csv(path)
        # self.ids.add_csv.on_release = self.process_csv(path)

    def exit_manager(self, *args):
        '''Exit the file manager.'''
        self.file_manager.close()

    def process_csv(self):
        '''Handle the selected CSV file, validate rows, and separate valid/invalid rows.'''
        
        if not self.path:
            return
        path = self.path
        self.contacts = []
        self.invalid_contact_input = []
        
        try:
            valid_rows = []
            invalid_rows = []
            file_name = os.path.basename(path)
            invalid_file_path = os.path.join(os.path.dirname(path), f"invalid_{file_name}")

            with open(path, mode='r') as file:
                csv_reader = csv.reader(file)
                
                for i, row in enumerate(csv_reader):
                    # Ensure row has exactly 2 columns
                    if len(row) != 2:
                        invalid_rows.append(row + [f"Error: Expected 2 columns, found {len(row)}"])
                        continue

                    id_number, phone_number = row

                    # Validate ID number (8 characters) and phone number (10 digits)
                    if len(id_number) == 8 and phone_number.isdigit() and len(phone_number) == 10:
                        valid_rows.append(row)
                    else:
                        error_msg = []
                        if len(id_number) != 8:
                            error_msg.append("ID must be 8 characters")
                        if not phone_number.isdigit() or len(phone_number) != 10:
                            error_msg.append("Phone number must be 10 digits")
                        invalid_rows.append(row + ["Error: " + ", ".join(error_msg)])

            # Store valid and invalid rows
            self.contacts = valid_rows
            self.invalid_contact_input = invalid_rows

            # If there are invalid rows, save them to a CSV file
            if invalid_rows:
                with open(invalid_file_path, mode='w', newline='') as invalid_file:
                    csv_writer = csv.writer(invalid_file)
                    # Write the invalid rows, possibly including error messages
                    csv_writer.writerow(["ID Number", "Phone Number", "Error Details"])  # Header
                    csv_writer.writerows(invalid_rows)
                # toast(f"Invalid contacts saved to {invalid_file_path}")

            # toast(f"Processed CSV. Valid: {len(valid_rows)}, Invalid: {len(invalid_rows)}")
            
            self.add_contacts(valid_rows)  
            
              

        except Exception as e:
            toast(f"Failed to open CSV: {str(e)}")
            
        self.path = None
        self.ids.file_name.text = 'Upload CSV file'
        
    def add_contacts(self, valid_contacts):
        
        id_numbers = []
        
        for contact in self.contacts:
            # print(contact)
            
            id_number, phone_number = contact
            
            # print(id_number)
            # print(phone_number)
            
            success, message, last_row_id = self.contact_controller.add_contact(id_number, phone_number)
            if success:
                # print(success, message, last_row_id)
                
                # # clear input fields
                # self.ids.id_number_field.text = ''
                # self.ids.phone_number_field.text = ''
                
                id_numbers.append(last_row_id)
                
                # display added contact on table
                # self.search_contact(id_number=last_row_id)
                
                
                # self.ids.add_contact_button.text = 'Add'
                
                # show notice
                self.notice.text = message
            else:
                self.notice.text = message
                # print(success, message, last_row_id)
        if len(id_numbers):
            self.search_contact(id_numbers=id_numbers)
            self.notice.text = f'{len(valid_contacts)} Contacts Uploaded Successfully'
            
    
    def add_contact(self,id_number, phone_number):
        self.notice.text = ''
        
        # print(id_number, ' ', phone_number)
        
        success, message, last_row_id = self.contact_controller.add_contact(id_number, phone_number)
        if success:
            # print(success, message, last_row_id)
            
            # clear input fields
            self.ids.id_number_field.text = ''
            self.ids.phone_number_field.text = ''
            
            # display added contact on table
            self.search_contact(id_number=last_row_id)
            
            
            self.ids.add_contact_button.text = 'Add'
            
            # show notice
            self.notice.text = message
        else:
            self.notice.text = message
            # print(success, message, last_row_id)

    def refocus_qr_code(self, *args):
        # Set focus back to the MDTextField after the delay
        self.ids.qr_code.focus = True
        
    def schedule_validation(self):
        # Cancel any previously scheduled validation
        qr_code = self.ids.qr_code.text
        if not qr_code:
            Clock.schedule_once(self.refocus_qr_code, 0.1)
            return
            
        if self.validation_event and self.validation_event.is_triggered:
            self.validation_event.cancel()
        
        # Schedule validation to run after a brief delay
        self.validation_event = Clock.schedule_once(self.search_contact, 0.2)

    def search_contact(self, qr_code=None, id_number=None, id_numbers=None):
        self.notice.text = ''
        
        
        # print(qr_code, id_number, id_numbers)
        # return
        if id_number:
        
            success, message, contacts = self.contact_controller.search_contact(id_number=id_number)
            
            # print(success, ' ', message, ' ', contact)
            if success:
                if contacts:
                    self.update_row_data(self.data_tables, contacts)
                    self.notice.text = "Search Results found"
                else:
                    self.notice.text = "No Results found"
                self.ids.id_number_field1.text = ''
            else:
                # self.notice.text = 'Something went wrong while searching for contacts, Contact Administrator'
                self.notice.text = message
                    
        elif id_numbers:
            success, message, contacts = self.contact_controller.search_contact(id_numbers=id_numbers)
            
            # print(success, ' ', message, ' ', contact)
            if success:
                if contacts:
                    self.update_row_data(self.data_tables, contacts)
                    self.notice.text = "Search Results found"
                else:
                    self.notice.text = "No Results found"
                self.ids.id_number_field1.text = ''
            else:
                self.notice.text = message    
                
        else: 
            qr_code = self.ids.qr_code.text
            if not qr_code:
                return
            code = QRCode(qr_code)
            success, message, id = code.process()
            if success:
                # print(id['id_number'])
                self.search_contact(id_number=id['id_number'])
            else:
                self.notice.text = message
                
            Clock.schedule_once(self.refocus_qr_code, 0.1)
            self.ids.qr_code.text = ''
        
    def update_row_data(self, instance_data_table, search_results):
        """
        Updates the row data of the given data table instance.

        :param instance_data_table: The instance of the data table to update.
        :param search_results: Raw data from search results.
        """
        
        
        try:
            # Transform the search results to match the datatable format
            self.data = self.transform_data_for_datatable(search_results)
            
            # print(data)
            # return
            
            # Clear the existing row data and signature map
            instance_data_table.row_data = []
            # self.id_map.clear()
            
            # Reset progress variables for adding rows
            self.current_row_index = 0
            self.total_rows = len(self.data)
            self.search_results = search_results
            
            # Start adding rows one by one using Clock.schedule_interval
            Clock.schedule_interval(self.add_row_one_by_one, .5)  # Adjust time for speed
        
        except ValueError as e:
            self.notice.text = f"Error: {e}. from {__name__}"
            
        # self.progress.active = False
        
    def transform_data_for_datatable(self, search_results):
        """
        Transforms search results into the format required by MDDataTable.

        :param search_results: A list of dictionaries containing search results.
        :return: A list of lists containing only the necessary columns for MDDataTable.
        """
        # Define the columns to include in the datatable
        required_columns = ['id_number', 'phone_number']
        
        # print(search_results)
        
        # Transform the data
        transformed_data = []
        for result in search_results:
            row = [result.get(col, '') for col in required_columns]
            # row.append(f'')
            transformed_data.append(row)
        
        return transformed_data  
    
    def add_row_one_by_one(self, dt):
        """Adds one row to the table at a time."""
        
        self.current_page = 1
        
        if self.current_row_index < self.total_rows:
            # Add the next row
            row = self.data[self.current_row_index]
            self.data_tables.add_row(row)
            
            # self.id_map[self.current_row_index] = {}

            # # Store the signature for the row
            # self.id_map[self.current_row_index]["signature"] = self.search_results[self.current_row_index].get('signature', '')
            # self.id_map[self.current_row_index]["batch"] = self.search_results[self.current_row_index].get('batch', '')

            # Increment the row index
            self.current_row_index += 1
        else:
            # Stop the interval once all rows are added
            return False 
    
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        
        try:
            
            # Get the index of the pressed row
            columns_per_row = len(instance_table.column_data)
            cell_index = instance_row.index
            if cell_index:
                local_row_index = cell_index // columns_per_row
            else:
                local_row_index = cell_index
                
            # Get pagination info
            rows_per_page = instance_table.rows_num    # Number of rows per page
            current_page = self.current_page  # Current page number

            # Calculate the global row index
            global_row_index = (current_page - 1) * rows_per_page + local_row_index

            # print(f"Local cell index: {cell_index}")
            # print(f"Local row index: {local_row_index}")
            # print(f"Rows per page: {rows_per_page}")
            # print(f"Current page: {current_page}")
            # print(f"Global row index: {global_row_index}")

            # Get the global row data
            row_data = instance_table.row_data[global_row_index]
            # print(f"Row data: {row_data}")
            
            self.ids.id_number_field.text = row_data[0]
            self.ids.phone_number_field.text = row_data[1]
            self.ids.add_contact_button.text = 'Update'
            
        except IndexError as e:
            print(f"IndexError occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
            