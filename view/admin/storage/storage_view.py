from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
# from kivymd.uix.list import OneLineListItem, OneLineAvatarListItem

from controller.storage_unit_controller import StorageUnitController


# Builder.load_file('view/UI.kv')
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

Builder.load_file(resource_path('storage_view.kv'))
# Builder.load_file('view/admin/storage/storage_view.kv')
# Builder.load_file('C:\\Users\\HKay\\PycharmProjects\\NID_Inventory\\view/admin/storage/storage_view.kv')


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
        
        self.add_dialog = None
        self.delete_dialog = None
        
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
            card.bind(on_release=lambda card_instance, s_id=storage_id, s_label=storage_label, count=total_count : self.on_card_click(card_instance, s_id, s_label, count))
            
            self.ids.storage_unit_grid.add_widget(card)
        # self.progress.active = False
        
    def update_grid_cols(self, layout, *args):
        # Card width + spacing between cards
        card_width_with_spacing = dp(132)
        available_width = layout.width
        
        # Calculate and update the number of columns based on the available width
        cols = max(1, int(available_width // card_width_with_spacing))
        # print(f"cols: {cols} Card width with spacing: {card_width_with_spacing} Parent width: {available_width}")
        self.ids.storage_unit_grid.cols = cols
        
    def on_card_click(self, card_instance, storage_id, storage_label, count):
        self.notice.text = ''
        
        if count > 0:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = 'Only empty storage units can be marked for deletion'
            return
        
        # Reset the background color of the previously selected card, if any
        if f'Unit: {storage_label}' in self.selected_storage_ids:
            card_instance.md_bg_color = self.app.theme_cls.bg_light
            del self.selected_storage_ids[f'Unit: {storage_label}']
            # print(self.selected_storage_ids)
            return
        
        
        # Change background color of the clicked card to primary color
        card_instance.md_bg_color = self.app.theme_cls.primary_color 

        # Store the clicked card as selected card
        # self.selected_card = card_instance
        
        # # Assign storage_label to allocated storage input field
        # self.ids.allocated_storage.text = storage_label
        
        # # Assign storage_id to a variable
        self.selected_storage_ids[f'Unit: {storage_label}'] = storage_id
        # print(self.selected_storage_ids)
        
    # def delete_selected(self, *args):
    #     storage_ids = []
    #     for id in self.selected_storage_ids:
    #         storage_ids.append(id)
            
    def open_add_dialog(self):
        self.add_dialog = None
        if not self.add_dialog:
            # Create an input field for number of storage units
            self.add_dialog = MDDialog(
                title="Add Storage Units",
                size_hint=(None, None),
                size = (dp(380), dp(480)),
                type="custom",
                content_cls=MDTextField(
                    hint_text="Number of storage units to be added",
                    input_filter="int",  # Only accept integer input
                    mode="rectangle",
                    icon_left = 'numeric',
                ),
                buttons=[
                    MDFlatButton(
                        text="Cancel", on_release=lambda x: self.add_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="Add",
                        on_release=lambda x: self.add_storage_units()
                    ),
                ],
            )
        self.add_dialog.open()

    def open_delete_dialog(self):
        self.delete_dialog = None
        
        if not self.delete_dialog:
            # Get the list of storage units marked for deletion
            storage_units = list(self.selected_storage_ids.keys())
            
            if not storage_units:
                self.notice.color = self.app.theme_cls.error_color
                self.notice.text = 'Select at least one unit for deletion'
                return
            
            # Create a vertical layout and add each storage unit as an MDLabel
            # content = MDBoxLayout(orientation="vertical", spacing="12dp", padding="20dp")
            # row = MDBoxLayout(orientation="horizontal", spacing="12dp", padding="20dp")
            
            units = ''
            counter = 0
            for unit in storage_units:
                counter += 1
                units += f'{unit},    '
                if counter % 6 == 0:
                    units += f'\n'
                # row.add_widget(MDLabel(text=unit, halign="left"))
            # content.add_widget(row)
            
            # Set up the dialog with the labels as content
            self.delete_dialog = MDDialog(
                title="Delete Selected Storage Units",
                text=f"Are you sure you want to Delete Selected Storage Units?\n\n{units}",
                # type="custom",
                auto_dismiss=False,
                size_hint=(None, None),
                size = (dp(480), dp(480)),
                # content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="Cancel", 
                        on_release=lambda x: self.delete_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="Delete",
                        on_release=lambda x: self.delete_selected()
                    ),
                ],
            )

        # Open the dialog
        self.delete_dialog.open()
        
    def add_storage_units(self):
        # Logic to add storage units
        num_units = int(self.add_dialog.content_cls.text)
        # print(f"Adding {num_units} storage units")
        
        success, message, data = self.storage_unit_controller.create_storage_units(num_units)
        if success:
            self.notice.color = [0, 1, 0, 1] 
            self.notice.text = f'{num_units} New Storage Units Added'
            Clock.schedule_once(self.populate_storage_units, 0.1)
        else:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = f'Error while adding storage, contact admin'
            
        
        self.add_dialog.dismiss()

    def delete_selected(self):
        # Logic to delete selected storage units
        # print("Deleting selected storage units")
        ids = list(self.selected_storage_ids.values())
        
        success, message, data = self.storage_unit_controller.delete_storage_units(ids)
        if success:
            self.notice.color = [0, 1, 0, 1] 
            self.notice.text = f'{len(self.selected_storage_ids)} Storage Units Deleted Successfuly'
            Clock.schedule_once(self.populate_storage_units, 0.1)
        else:
            self.notice.color = self.app.theme_cls.error_color
            self.notice.text = f'Error while deleting storage units, contact admin'
            print(message)
        
        self.selected_storage_ids = {}
        self.delete_dialog.dismiss()