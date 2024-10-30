from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


from controller.storage_unit_controller import StorageUnitController


# Builder.load_file('view/UI.kv')
Builder.load_file('view/admin/storage/storage_view.kv')


class StorageScreen(Screen):
    def __init__(self, **kwargs):
        super(StorageScreen, self).__init__(**kwargs)
        self.storage_unit_controller = StorageUnitController()
        self.app = MDApp.get_running_app()
        
        # self.progress = self.app.root.ids.progress
        self.notice = self.app.root.ids.notice
        # self.controller = UserController()
        self.selected_card = None  # To track the currently selected card
        self.selected_storage_ids = {}  # Variable to store selected storage_id
        
        Clock.schedule_once(self.populate_storage_units, 0.1)
        

    def populate_storage_units(self, *args):
        # self.progress.active = True
        # Clear existing widgets
        self.ids.storage_unit_grid.clear_widgets()
        
        # Fetch storage units and counts
        success, message, storage_units = self.storage_unit_controller.get_storage_units('id')
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
            card = MDCard(size_hint=(None, None), size=(dp(120), dp(100)), elevation=1, radius=[10])
            card_box = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))

            # Add label and total count to the card
            card_box.add_widget(MDLabel(text=f"Unit: {storage_label}", halign='center', theme_text_color="Primary"))
            card_box.add_widget(MDLabel(text=f"ID Count: {total_count}", halign='center', theme_text_color="Secondary"))

            card.add_widget(card_box)
            
            # Add click behavior to the card
            card.bind(on_release=lambda card_instance, s_id=storage_id, s_label=storage_label: self.on_card_click(card_instance, s_id, s_label))
            
            self.ids.storage_unit_grid.add_widget(card)
        # self.progress.active = False
        
    def update_grid_cols(self, layout, *args):
        # Card width + spacing between cards
        card_width_with_spacing = dp(130)
        available_width = layout.width
        
        # Calculate and update the number of columns based on the available width
        cols = max(1, int(available_width / card_width_with_spacing))
        # print(f"cols: {cols} Card width with spacing: {card_width_with_spacing} Parent width: {available_width}")
        self.ids.storage_unit_grid.cols = cols
        
    def on_card_click(self, card_instance, storage_id, storage_label):
        # Reset the background color of the previously selected card, if any
        if storage_id in self.selected_storage_ids:
            card_instance.md_bg_color = self.app.theme_cls.bg_light
            del self.selected_storage_ids[storage_id]
            print(self.selected_storage_ids)
            return
        
        # Change background color of the clicked card to primary color
        card_instance.md_bg_color = self.app.theme_cls.primary_color 

        # Store the clicked card as selected card
        # self.selected_card = card_instance
        
        # # Assign storage_label to allocated storage input field
        # self.ids.allocated_storage.text = storage_label
        
        # # Assign storage_id to a variable
        self.selected_storage_ids[storage_id] = storage_id
        print(self.selected_storage_ids)
        
        