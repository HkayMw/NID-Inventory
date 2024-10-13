from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
import csv
import os

from Assets.qr_code import QRCode
from controller.contact_controller import ContactController

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/contact/contact_view.kv')


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

    def on_enter(self, *args):
        Clock.schedule_once(self.initialize_table, 0.5)
        # print(self.parent.current)
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        
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
                ("Action", dp(40)),
            ],
            row_data=[]
        )
       
        # self.ids.lastname_field.text = "something"
        self.ids.table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.table_container.add_widget(layout)
        # print(self.root)
        
        
    def open_file_manager(self):
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

        # Call a function to process the CSV file
        self.process_csv(path)

    def exit_manager(self, *args):
        '''Exit the file manager.'''
        self.file_manager.close()

    def process_csv(self, path):
        '''Handle the selected CSV file, validate rows, and separate valid/invalid rows.'''
        
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
                toast(f"Invalid contacts saved to {invalid_file_path}")

            toast(f"Processed CSV. Valid: {len(valid_rows)}, Invalid: {len(invalid_rows)}")

        except Exception as e:
            toast(f"Failed to open CSV: {str(e)}")
            
    def add_contacts(self):
        
        pass
    
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
            
            # show notice
            self.notice.text = message
        else:
            self.notice.text = message
            # print(success, message, last_row_id)

    def search_contact(self, qr_code=None, id_number=None):
        self.notice.text = ''
        
        
        # print(qr_code, id_number)
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
                self.notice.text = message
                    
            
                
        if qr_code:
            code = QRCode(qr_code)
            success, message, id = code.process()
            if success:
                print(id['id_number'])
                self.search_contact(id_number=id['id_number'])
            else:
                self.notice.text = message
                
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
            Clock.schedule_interval(self.add_row_one_by_one, 1)  # Adjust time for speed
            return
            
            # Update the table with new row data and store the signature separately
            for index, row in enumerate(data):
                instance_data_table.add_row(row)
                # Store the signature in the signature map
                self.id_map[index] = search_results[index].get('signature', '')
            #     print(f"Row {index} added with hidden signature: {self.id_map[index]}")
            # print(f"Row data updated successfully.\nSignature Map {self.id_map}")
        
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
  