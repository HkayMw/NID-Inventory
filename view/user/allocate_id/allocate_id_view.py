from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

import qrcode
from io import BytesIO
import qrcode
from PIL import Image as PILImage, ImageDraw, ImageFont
from Assets.label_printer import LabelPrinter

from controller.user_controller import UserController
from controller.batch_controller import BatchController
from controller.storage_unit_controller import StorageUnitController
from controller.id_controller import IdController

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/allocate_id/allocate_id_view.kv')


class AllocateIDScreen(Screen):
    def __init__(self, **kwargs):
        super(AllocateIDScreen, self).__init__(**kwargs)
        self.batch_controller = BatchController()
        self.storage_unit_controller = StorageUnitController()
        self.id_controller = IdController()
        self.label_controller= LabelPrinter()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        # self.notice.text = ''
        
        self.progress = self.app.root.ids.progress
        self.selected_card = None  # To track the currently selected card
        self.storage_id = None  # Variable to store selected storage_id
        
    def on_enter(self, *args):
        # self.initialize_allocate_storage_table()
        self.current_user = self.app.user_details
        self.user_id = self.current_user['id_number']
        
        
        self.ids.count.text = str(len(self.app.current_batch['ids']))
        self.ids.batch_name.text = self.app.current_batch['batch_name']
        # self.ids.allocated_storage.text = '[b][color=#ff6688]Please select storage unit[/color][/b]'
        self.ids.allocated_storage.text = ''
        
        # print(f"storage_id: {self.storage_id} selected card: {self.selected_card}")
        # Load Storage units
        # self.storage_unit_controller.get_storage_units()
        # self.populate_storage_units()
        Clock.schedule_once(self.populate_storage_units, 0.1)
    
        
    def on_leave(self, *args):
        self.ids.qr_card.clear_widgets()
        self.ids.storage_unit_grid.clear_widgets()
        # self.app.current_batch = {"batch_name": '', "ids": []}
        return super().on_leave(*args)
    
    def populate_storage_units(self, *args):
        self.progress.active = True
        # Clear existing widgets
        self.ids.storage_unit_grid.clear_widgets()
        
        # Fetch storage units and counts (mocked for this example)
        success, message, storage_units = self.storage_unit_controller.get_storage_units()
        # print(storage_units)
        # return
        for unit in storage_units:
            storage_id = unit['id']
            storage_label = unit['label']
            total_count = unit['count']
            if not total_count:
                total_count = 0
            
            # print(unit)
            
            # Create MDCards for each storage unit
            card = MDCard(size_hint=(None, None), size=(dp(140), dp(100)), elevation=1, radius=[10])
            card_box = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))

            # Add label and total count to the card
            card_box.add_widget(MDLabel(text=f"Unit: {storage_label}", halign='center', theme_text_color="Primary"))
            card_box.add_widget(MDLabel(text=f"ID Count: {total_count}", halign='center', theme_text_color="Secondary"))

            card.add_widget(card_box)
            
            # Add click behavior to the card
            card.bind(on_release=lambda card_instance, s_id=storage_id, s_label=storage_label: self.on_card_click(card_instance, s_id, s_label))
            
            self.ids.storage_unit_grid.add_widget(card)
        self.progress.active = False
            
 
    def on_card_click(self, card_instance, storage_id, storage_label):
        # Reset the background color of the previously selected card, if any
        if self.selected_card:
            self.selected_card.md_bg_color = [1, 1, 1, 1]  # White background
        
        # Change background color of the clicked card to primary color
        card_instance.md_bg_color = self.app.theme_cls.primary_color 

        # Store the clicked card as selected card
        self.selected_card = card_instance
        
        # Assign storage_label to allocated storage input field
        self.ids.allocated_storage.text = storage_label
        
        # Assign storage_id to a variable
        self.storage_id = storage_id    
    
    def update_grid_cols(self, layout, *args):
        # Card width + spacing between cards
        card_width_with_spacing = dp(170)
        available_width = layout.width
        
        # Calculate and update the number of columns based on the available width
        cols = max(1, int(available_width / card_width_with_spacing))
        # print(f"cols: {cols} Card width with spacing: {card_width_with_spacing} Parent width: {available_width}")
        self.ids.storage_unit_grid.cols = cols
    
    # def initialize_allocate_storage_table(self):
    #     # Initialize the table with default headers and an empty state
    #     layout = AnchorLayout()
    #     self.data_tables = MDDataTable(
    #         use_pagination=True,

    #         check=True,
    #         column_data=[
    #             ("Storage Unit", dp(40)),
    #             ("ID Count", dp(40)),
    #             ("Action", dp(20)),
    #         ],
    #         row_data=[]
    #     )
       

    #     self.ids.allocate_storage_table_container.clear_widgets()
    #     layout.add_widget(self.data_tables)
    #     self.ids.allocate_storage_table_container.add_widget(layout)
        
    def add_batch(self):
        self.progress.active = True
        
        
        current_batch = self.app.current_batch
        
        if not current_batch['ids']:
            # self.label_controller.print_label()
            self.notice.text = "There are no new IDs to add"
            return
        
        # print(current_batch)
        # get batch name and count
        batch_name = self.ids.batch_name.text
        count = int(self.ids.count.text)
        
        storage = self.storage_id
        qr_text = f"Batch Name: {batch_name}, Allocated Storage: {storage}"
        user_id = self.user_id
        
        if not storage:
            # todo: make notice alert color
            self.notice.text = F"Please select storage unit first"
            self.progress.active = False
            return
        # # keep batch name
        # current_batch['batch_name'] = batch_name
        
        success, message, batch = self.batch_controller.add_batch(batch_name, count, storage, qr_text, user_id)
        if success:
            batch = batch
            self.notice.text = message
            self.app.current_batch = {"batch_name": '', "ids": []}
            # self.progress.active = False
            # print(batch)
            
        else:
            self.notice.text = message
            self.label_controller.print_label()
            self.progress.active = False
            return
        
        added = 0
        for id in current_batch["ids"]:
            
            id = {**id, "batch": batch}
            #Add id
            try:
                success, message, record_id = self.id_controller.add_id(id)
                # print(self.controller.add_id(id))
                if success:
                    self.notice.text = F"{message} {id['id_number']}"
                    added = added + 1
                    
                elif message == "An error occurred: UNIQUE constraint failed: id.id_number, id.issue_date":
                    self.notice.text = f"This record with ID Number: {id['id_number']} already exists in the database."
                    self.progress.active = False
                    return
                    
                else:
                    self.notice.text = message
                    self.progress.active = False
                    return
                    
            except Exception as e:
            # print(f"An unexpected error occurred: {e}")    
                self.notice.text = f"An unexpected error occurred: {e}"
                self.progress.active = False
                #
        if added == len(current_batch['ids']):
            # todo: make notice success color
            self.notice.text = "Batch added successfully"
            Clock.schedule_once(self.populate_storage_units, 0.1)
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

            # Add the image to the layout
            self.ids.qr_card.clear_widgets()
            self.ids.qr_card.add_widget(qr_image_widget)
            
            self.print_sticker(img, data)
        # self.notice.text = notice
        self.progress.active = False
        
    def print_sticker(self, img, data):
        
        success, message, label_data = self.label_controller.make_label(img, data)
        if success:
            print(message)
            print(label_data)
            
            success, message, result = self.label_controller.print_label(label_data['file_path'], label_data['label_width'], label_data['label_height'])
        

class Tab(BoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass


    
    