from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
# from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock
from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout 
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from controller.user_controller import UserController

# Builder.load_file('view/UI.kv')
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('manage_user_view.kv'))
# Builder.load_file('view/admin/userManagement/manage_user_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/admin/userManagement/manage_user_view.kv')


class ManageUser(Screen):
    def __init__(self, **kwargs):
        super(ManageUser, self).__init__(**kwargs)
        self.user_controller = UserController()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        
        self.ids.add_user_button.bind(on_release=self.add_user)
        # self.selected_role = None
        Clock.schedule_once(self.initialize_table, 0.2)


    def on_enter(self, *args):
        # self.initialize_table()
        Clock.schedule_once(self.search_user, 0.5)
        Clock.schedule_once(self.clear_notice, 0.5)
        
        self.clicked_user_row = None
        
    def on_leave(self, *args):
        self.clear_fields()
        return super().on_leave(*args)
        
    def clear_notice(self, *args):
        self.notice.text = ''
    
    # def set_role(self, role):
    #     self.selected_role = role
    #     print(f"Selected role: {self.selected_role}")   
        
    def initialize_table(self, *args):
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            use_pagination=True,
            # check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("ID Number", dp(20)),
                ("Surname", dp(20)),
                ("Firstname", dp(20)),
                ("Othernames", dp(20)),
                ("Role", dp(20)),
                ("created_by", dp(20)),
                ("updated_by", dp(20)),
            ],
            row_data=[]
        )
        
        # self.ids.lastname_field.text = "something"
        self.ids.table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.table_container.add_widget(layout)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        

    def add_user(self, *args):
        
        id_number = self.ids.id_number_field.text.upper()
        firstname = self.ids.firstname_field.text.upper()
        surname = self.ids.lastname_field.text.upper()
        othernames = self.ids.othernames_field.text.upper()
        password1 = self.ids.password_field.text
        password2 = self.ids.password_field1.text
        
        if not id_number:
            self.notice.text = 'ID Number is Required'
            return
        
        if not (len(id_number) == 8):
            self.notice.text = 'Invalid ID Number'
            return
            
        if not firstname:
            self.notice.text = 'Firstname is Required'
            return
            
        if not surname:
            self.notice.text = 'Surname is Required'
            return
            
        if not password1:
            self.notice.text = 'Password is Required'
            return
            
        if not password2:
            self.notice.text = 'Please comfirm the password'
            return
            
        if password1 == password2:
            password = password1
        else:
            self.notice.text = 'Passwords dont match, please check'
            return
        
        role = None
        
        
        if self.ids.clerk_radio.active:
            role = "Clerk"
        elif self.ids.admin_radio.active:
            role = "Admin"

        if role:
            # print(f"Selected role: {role}")
            pass
        else:
            self.notice.text = 'Role is Required'
            return
            
        
        user_data={"id_number": id_number, "firstname": firstname, "lastname": surname, "othernames": othernames, "password": password, "user_type": role}
        
        success, message, user_id = self.user_controller.add_user(user_data)
        
        if success:
            self.clear_fields()
            self.search_user()
            self.notice.text = 'User Added Successfully'
        else:
            self.notice.text = 'Something went wrong trying to add user, contact Administrator'
            print(message)
            return
    
    def show_user_info_dialog(self):
        self.clear_fields()
        
        row_data = self.clicked_user_row
        if not row_data:
            return
        surname = row_data[1]
        firstname = row_data[2]
        othernames = row_data[3]
        id_number = row_data[0]
        
        if hasattr(self, 'user_info_dialog'):
            self.user_info_dialog = None

        # Create a new dialog instance every time
        self.user_info_dialog = MDDialog(
            title="Confirm User Details",
            text=f"\nSurname: {surname}\nFirstname: {firstname}\nOthernames: {othernames}\nID Number: {id_number}",
            size_hint=(0.3, 0.35),
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=self.close_user_info_dialog
                ),
                MDRaisedButton(
                    text="Remove User",
                    on_release=self.remove_user
                ),
                MDRaisedButton(
                    text="Edit User",
                    on_release=self.load_user_data
                )
            ]
        )
            
        self.user_info_dialog.open()

    def close_user_info_dialog(self, *args):
        self.user_info_dialog.dismiss()

    def update_user(self, *args):
        self.notice.text = ''
        
        id_number = self.ids.id_number_field.text.upper()
        firstname = self.ids.firstname_field.text.upper()
        surname = self.ids.lastname_field.text.upper()
        othernames = self.ids.othernames_field.text.upper()
        password1 = self.ids.password_field.text
        password2 = self.ids.password_field1.text
        
        if not id_number:
            self.notice.text = 'ID Number is Required'
            return
            
        if not firstname:
            self.notice.text = 'Firstname is Required'
            return
            
        if not surname:
            self.notice.text = 'Surname is Required'
            return
            
        if password1 or password2:
            if password1 == password2:
                password = password1
                
                # user_data = {**user_data, "password": password}
            else:
                self.notice.text = 'Passwords dont match, please check'
                return
        else:
            password = None
        
        role = None
        
        
        if self.ids.clerk_radio.active:
            role = "Clerk"
        elif self.ids.admin_radio.active:
            role = "Admin"

        if role:
            # print(f"Selected role: {role}")
            pass
        else:
            self.notice.text = 'Role is Required'
            return
        
        user_data={"id_number": id_number, "firstname": firstname, "lastname": surname, "othernames": othernames, "password": password, "user_type": role}
        
            
        success, message, user_id = self.user_controller.update_user(user_data)
        
        if success:
            self.clear_fields()
            # Enable the ID number field
            self.ids.id_number_field.disabled = False
            self.search_user()
            self.notice.text = 'User Updated successfully'
        else:
            self.notice.text = 'Something went wrong trying to update user, contact Administrator'
            print(message)
            return
        
        # clear selcted row data
        self.clicked_user_row = None
    
    def remove_user(self, *args):
        # self.clear_fields()
        self.close_user_info_dialog()
        id_number = self.clicked_user_row[0]
        if not id_number:
            return
        
        print('removed ', id_number)
        
        success, message, user = self.user_controller.remove_user(id_number)
        if success:
            self.search_user()
            self.notice.text = f'User: {user} Removed Successfully'
        else:
            self.notice.text = 'Something went wrong trying to remove user, contact Administrator'
            
        # clear selcted row data
        self.clicked_user_row = None
    
    def search_user(self, *args):
        self.notice.text = ''
        # clear selcted row data
        self.clicked_user_row = None
        
        firstname = self.ids.firstname_search_field.text.upper()
        surname = self.ids.surname_search_field.text.upper()
        id_number = self.ids.id_search_field.text.upper()
        
        if not (firstname or surname or id_number):
            success, message, users = self.user_controller.search_user()
            if success:
                if users:
                    self.clear_fields()
                    self.update_row_data(self.data_tables, users)
                    self.notice.text = "Search Results found"
                else:
                    self.data_tables.row_data = []
                    self.notice.text = 'No Users found'
            else:
                self.notice.text = 'Something went wrong while searching for users, Contact Administrator'
            
            # print(users)
        else:
            user_data = {}
            if firstname:
                user_data['firstname'] = firstname
            else:
                user_data['firstname'] = None
            if surname:
                user_data['surname'] = surname
            else:
                user_data['surname'] = None
            if id_number:
                user_data['id_number'] = id_number
                
                if not (len(id_number) == 8):
                    self.notice.text = 'Invalid ID Number'
                    return
            else:
                user_data['id_number'] = None
            
            
                
            success, message, users = self.user_controller.search_user(user_data)
            if success:
                if users:
                    self.clear_fields()
                    self.update_row_data(self.data_tables, users)
                    self.notice.text = "Search Results found"
                else:
                    self.data_tables.row_data = []
                    self.notice.text = 'No Users found'
            else:
                self.notice.text = 'Something went wrong while searching for users, Contact Administrator'
            
        pass
    
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
        required_columns = ['id_number', 'surname', 'firstname', 'othernames', 'user_type', 'created_by', 'updated_by']
        
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
        self.ids.admin_radio.active = False
        self.ids.clerk_radio.active = False

        
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
            
            self.clicked_user_row = row_data
            
            self.show_user_info_dialog()
            
            
        except IndexError as e:
            print(f"IndexError occurred: {e}. from {__name__}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. from {__name__}")
            
    def load_user_data(self, *args):
        self.close_user_info_dialog()
        row_data = self.clicked_user_row
        if not row_data:
            return
        
        self.ids.id_number_field.text = row_data[0]
        self.ids.firstname_field.text = row_data[2]
        self.ids.lastname_field.text = row_data[1]
        self.ids.othernames_field.text = row_data[3]
        
        # Disable the ID number field
        self.ids.id_number_field.disabled = True
        
        # Reset the button text and bind it back to add_user
        self.ids.add_user_button.text = 'Add'
        
        # Set the radio buttons for the role
        if row_data[4].lower() == 'clerk':
            self.ids.clerk_radio.active = True
        elif row_data[4].lower() == 'admin':
            self.ids.admin_radio.active = True

            
         # Update button text and bind to update_user
        self.ids.add_user_button.text = 'Update'
        
        # Unbind the add_user method and bind the update_user method
        self.ids.add_user_button.unbind(on_release=self.add_user)
        self.ids.add_user_button.bind(on_release=self.update_user)
            
    def clear_fields(self):
        # Clear all MDTextFields
        self.ids.id_number_field.text = ''
        self.ids.firstname_field.text = ''
        self.ids.lastname_field.text = ''
        self.ids.othernames_field.text = ''
        self.ids.password_field.text = ''
        self.ids.password_field1.text = ''
        self.ids.firstname_search_field.text = ''
        self.ids.surname_search_field.text = ''
        self.ids.id_search_field.text = ''
                      
        # Enable the ID number field
        self.ids.id_number_field.disabled = False
        
        # Clear role radio buttons (uncheck both)
        self.ids.clerk_radio.active = False
        self.ids.admin_radio.active = False
        
        # Reset the button text and bind it back to add_user
        self.ids.add_user_button.text = 'Add'
        
        # Unbind the update_user method and bind the add_user method
        self.ids.add_user_button.unbind(on_release=self.update_user)
        self.ids.add_user_button.bind(on_release=self.add_user)

        
