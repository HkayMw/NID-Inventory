from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
# from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
# from kivy.core.window import Window

from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import qrcode
from io import BytesIO
# from PIL import Image as PILImage, ImageDraw, ImageFont
from Assets.label_printer import LabelPrinter


from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

# from kivymd.uix.boxlayout import MDBoxLayout

# from controller.user_controller import UserController
from controller.id_controller import IdController
from controller.batch_controller import BatchController
from controller.storage_unit_controller import StorageUnitController

# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.datatables import MDDataTable
# from kivy.metrics import dp



# Builder.load_file('view/UI.kv')
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('search_id_view.kv'))
# Builder.load_file('view/user/search_id/search_id_view.kv')

class SearchIDScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        self.label_controller= LabelPrinter()
        self.batch_controller = BatchController()
        self.controller = IdController()
        self.storage_controller = StorageUnitController()
        self.app = MDApp.get_running_app()
        # self.progress = self.app.root.ids.progress
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        # self.notice.text = ''
        
        # Dictionary to store signatures by row index
        self.id_map = {}  # To store hidden signatures
        self.current_page = 1 
        Clock.schedule_once(self.initialize_table, 0.2)
        
        
    def on_enter(self, *args):
        # self.initialize_table()
        self.clicked_id_signature = None
        self.validation_scheduled = None
        self.validation_event = None
        self.clicked_id_batch = None
        self.clicked_id_data = None        
        self.printing_img = None
        self.printing_data = None

        
        self.ids.batch_name.text = ''
        self.ids.count.text = ''
        self.ids.allocated_storage.text = ''
        self.ids.qr_card.clear_widgets()
        
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        
        Clock.schedule_once(self.refocus_qr_code, 0.1)
        
        # print(dir(self.ids.qr_code))
        
        
        
        
    def on_leave(self, *args):
        self.ids.id_no_field.text = ''
        self.ids.firstname_field.text = ''
        self.ids.lastname_field.text = ''
        self.ids.qr_code.text = ''
        self.printing_img = None
        self.printing_data = None

        return super().on_leave(*args)

    def initialize_table(self, *args):
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            use_pagination=True,
            background_color_selected_cell=self.app.theme_cls.primary_color,
            elevation = 3,
            

            # check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Surname", dp(25)),
                ("Firstname", dp(20)),
                ("Othernames", dp(25)),
                ("D_O_B", dp(20)),
                ("ID Number", dp(20)),
                ("Sex", dp(20)),
                ("Status", dp(20)),
            ],
            row_data=[]
        )
        # self.background_color = [0.7, 0.7, 0.7, 1]

        # self.ids.lastname_field.text = "something"
        self.ids.table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.table_container.add_widget(layout)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        # Bind back button
        self.data_tables.pagination.ids['button_back'].bind(on_release=lambda x: self.update_page(-1))
        
        # Bind forward button
        self.data_tables.pagination.ids['button_forward'].bind(on_release=lambda x: self.update_page(1))

    def update_page(self, change):
        """Update the current page of the data table."""
        # Ensure that change is either +1 for forward or -1 for back
        new_page = self.current_page + change
        self.current_page = new_page

    def refocus_qr_code(self, *args):
        # Set focus back to the MDTextField after the delay
        self.ids.qr_code.focus = True
        
    def schedule_validation(self, search_type):
        # Cancel any previously scheduled validation
        qr_code = self.ids.qr_code.text
        if not qr_code:
            return
        if self.validation_event and self.validation_event.is_triggered:
            self.validation_event.cancel()
        
        # Schedule validation to run after a brief delay
        self.validation_event = Clock.schedule_once(lambda dt: self.search_id(search_type), 0.2)
        
    def search_id(self, search_type, *args):
        # print(1)
        
        
        # Clear notice
        notice = self.notice
        # notice.theme_text_color = "Error"
        notice.text = ''
        # self.progress.active = True
        self.current_page = 1
        
        search_results = []
        if search_type == 'id':
            id_number = self.ids.id_no_field.text
            
            success, message, search_results = self.controller.search_id(search_type='id', id_number=id_number)
            if not success:
                # notice.theme_text_color = "Error"
                notice.text = message
                
            else:
                notice.text = message
            
            #clear ID Number input field    
            self.ids.id_no_field.text = ''

        elif search_type == 'name':
            firstname = self.ids.firstname_field.text
            lastname = self.ids.lastname_field.text
            
            
            success, message, search_results = self.controller.search_id(search_type='name', firstname=firstname, lastname=lastname)
            if not success:
                # notice.theme_text_color = "Secondary"
                notice.text = message
            else:
                #todo: change to green
                notice.text = message
                
            self.ids.firstname_field.text = ''
            self.ids.lastname_field.text = ''

        elif search_type == 'qr_code':
            qr_code = self.ids.qr_code.text
            if not qr_code:
                return
            success, message, search_results = self.controller.search_id(search_type='qr_code', qr_code=qr_code)
            if not success:
                # notice.theme_text_color = "Error"
                notice.text = message
                Clock.schedule_once(self.refocus_qr_code, 0.1)
            self.ids.qr_code.text = ''
        
        # Update table with search results
        if search_results:
            # print(len(search_results))
            self.update_row_data(self.data_tables, search_results)
            notice.text = message
            Clock.schedule_once(self.refocus_qr_code, 0.1)
        else:
            # Clear the current row data
            self.data_tables.row_data =[]
            
            Clock.schedule_once(self.refocus_qr_code, 0.1)
            # Also clear the signature map
            self.id_map.clear()
            
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
            self.id_map.clear()
            
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
        required_columns = ['lastname', 'firstname', 'othernames', 'd_o_b', 'id_number', 'gender', 'status']
        
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
            
            self.id_map[self.current_row_index] = {}

            # Store the signature for the row
            self.id_map[self.current_row_index]["signature"] = self.search_results[self.current_row_index].get('signature', '')
            self.id_map[self.current_row_index]["batch"] = self.search_results[self.current_row_index].get('batch', '')

            # Increment the row index
            self.current_row_index += 1
        else:
            # Stop the interval once all rows are added
            return False 
        
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        # print(f"Instance Table {instance_table}\nInstance Row {instance_row}")
        
        self.clicked_id_signature = None
        self.clicked_id_batch = None
        self.clicked_id_data = None
        self.printing_img = None
        self.printing_data = None


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

            # Get the global row data
            self.clicked_id_data = row_data = instance_table.row_data[global_row_index]
            print(f"Row data: {row_data}")
            
            # Validate the index
            if 0 <= global_row_index < len(instance_table.row_data):
                # Get the data of the pressed row
                
                # Retrieve the 'signature' from the corresponding search results
                self.clicked_id_signature = self.id_map[global_row_index]['signature'] 
                self.clicked_id_batch = self.id_map[global_row_index]['batch']  
                # print(f"Signature: {self.clicked_id_signature}\nBatch: {self.clicked_id_batch}")
                
                success, message, batch = self.batch_controller.get_batch(id=self.clicked_id_batch)
                
                # print(f"Success: {success}\nMessage: {message}\nBatch: {batch}")
                
                if success:
                    batch_name = self.ids.batch_name.text = batch['name']
                    batch_count = self.ids.count.text = str(batch['count'])
                    
                    success, message, storage = self.storage_controller.get_storage_unit(id=batch['storage'])
                    
                    if success:
                        allocated_storage = self.ids.allocated_storage.text = str(storage['label'])
                    else:
                        print(message)
                        return
                    
                    
                    
                else:
                    print(message)
                    return
                
                qr_text = f'Batch Name: {batch_name}, Allocated Storage: {allocated_storage}'
                
                # Data to encode
                data = qr_text

                # Create QR code instance
                qr = qrcode.QRCode(
                    version=1,  # Controls the size of the QR code. Higher number means bigger code.
                    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
                    box_size=10,  # Size of each box in the QR code
                    border=2,  # Thickness of the border
                )

                # Add data to the QR code
                qr.add_data(data)
                qr.make(fit=True)

                # Create an image from the QR code
                img = qr.make_image(fill="black", back_color="white")

                # # Save the image
                # img.save("qrcode_example.png")
                # self.print_qr_code(img)
                
                # Convert the image to a Kivy-compatible format
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)

                # Load the image as Kivy CoreImage
                kivy_image = CoreImage(buffer, ext="png")

                # Create an Image widget to display the QR code
                qr_image_widget = Image(texture=kivy_image.texture)
                # print(dir(qr_image_widget))

                # Add the image to the layout
                self.ids.qr_card.clear_widgets()
                # qr_image_widget.bind(on_release = lambda x, y: self.print_sticker(img, data))
                self.ids.qr_card.add_widget(qr_image_widget)
                
                self.printing_img = img
                self.printing_data = data
                
                
                
                
            else:
                print("Invalid row index or row data not found.")
        
        except IndexError as e:
            print(f"IndexError occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def show_issue_id_dialog(self):
        row_data = self.clicked_id_data
        if not row_data:
            return
        surname = row_data[0]
        firstname = row_data[1]
        othernames = row_data[2]
        dob = row_data[3]
        id_number = row_data[4]
        sex = row_data[5]
        
        if hasattr(self, 'issue_id_dialog'):
            self.issue_id_dialog = None

        # Create a new dialog instance every time
        self.issue_id_dialog = MDDialog(
            title="Confirm ID Details",
            text=f"Are you sure you want to Issue this ID?\n\nSurname: {surname}\nFirstname: {firstname}\nOthernames: {othernames}\nDate of Birth: {dob}\nSex: {sex}\nID Number: {id_number}",
            # size_hint=(0.4, 0.4),
            size_hint=(None, None),
            size = (dp(480), dp(480)),
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=self.close_issue_id_dialog
                ),
                MDRaisedButton(
                    text="Confirm",
                    on_release=self.issue_id
                )
            ]
        )
            
        self.issue_id_dialog.open()

        
    def close_issue_id_dialog(self, instance):
        self.clicked_id_signature = None
        self.clicked_id_batch = None
        self.clicked_id_data = None
        
        self.ids.batch_name.text = ''
        self.ids.count.text = ''
        self.ids.allocated_storage.text = ''
        self.ids.qr_card.clear_widgets()
        
        self.issue_id_dialog.dismiss()

        
    def issue_id(self, instance):
        signature = self.clicked_id_signature
        print(f"Attempting to issue ID with signature: {signature}")  # Debug statement

        if signature is None:
            print("No signature found. Cannot issue ID.")
            return  # Exit if there's no signature

        success, message, row = self.controller.issue_id(signature)

        if success:
            print(f"ID issued successfully: {message}")
            
            success, message, id = self.controller.search_id(search_type='signature', signature=signature)
            # Update table with search results
            if id:
                # print(len(search_results))
                self.update_row_data(self.data_tables, id)
                
            self.notice.text = "ID issued successfully"
            self.ids.qr_card.clear_widgets()
            
        else:
            print(f"Failed to issue ID: {message}")
            self.notice.text = "Something went wrong trying to issue an ID"

        self.close_issue_id_dialog(instance)   


    def print_sticker(self):
        print('printing')
        img = self.printing_img
        data = self.printing_data
        if not img:
            return
        if not data:
            return
        
        success, message, label_data = self.label_controller.make_label(img, data)
        if success:
            print(message)
            print(label_data)
            
            success, message, result = self.label_controller.print_label(label_data['file_path'], label_data['label_width'], label_data['label_height'])




