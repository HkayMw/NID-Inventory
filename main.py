from kivy.config import Config

# Set the default window size
default_width = 1024
default_height = 600

# Config.set('graphics', 'width', str(default_width))
# Config.set('graphics', 'height', str(default_height))


from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from datetime import datetime

# KivyMD
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton, MDTextButton, MDFillRoundFlatIconButton
from kivymd.uix.pickers import MDDatePicker

# from model.current_user import CurrentUser

# Importing navigation views
from view.navigation.clerk_nav import ClerkNav
from view.navigation.admin_nav import AdminNav

# Importing custom screens
from view.login.login_view import LoginScreen
from view.user_profile.user_profile_view import ProfileScreen

from view.user.dashboard.dashboard_view import DashboardScreen
from view.user.search_id.search_id_view import SearchIDScreen
from view.user.add_id.add_id_view import AddIDScreen
from view.user.allocate_id.allocate_id_view import AllocateIDScreen
# from view.user.sort_id.sort_id_view import SortIDScreen
from view.user.contact.contact_view import ContactScreen
from view.admin.storage.storage_view import StorageScreen

from view.admin.adminDashboard.adminDashboard_view import AdminDashboardScreen
from view.admin.userManagement.manage_user_view import ManageUser
from view.admin.configuration.config_view import ConfigScreen
from view.admin.notifyClient.notify_view import NotifyScreen
from view.admin.report.report_view import ReportScreen

# Set the minimum size to be the same as the default size
Window.minimum_width = default_width
Window.minimum_height = default_height


# Function to force layout refresh
def refresh_layout(*args):
    Window.size = (default_width + 1, default_height + 1)  # Temporary resize to force refresh
    Window.size = (default_width, default_height)  # Reset to desired size


# # Schedule a layout refresh on the next frame
# Clock.schedule_once(refresh_layout, 0.1)

# Define MainScreen as a ScreenManager
class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the transition
        self.ids.screen_manager.transition = NoTransition()
        # Bind the on_key_down event
        Window.bind(on_key_down=self.on_key_down)

    # Focus management function
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # print(f"Keycode: {keycode}, Text: {text}, Modifiers: {modifiers}")
        if keycode == 43:  # Assuming 43 is the keycode you want to handle
            # Collect all focusable widgets
            focusable_widgets = [w for w in self.walk(restrict=True) if hasattr(w, 'focus') and w.is_focusable]

            # Find the currently focused widget
            focused_widget = next((w for w in focusable_widgets if w.focus), None)
            if focused_widget:
                # Find the index of the focused widget
                index = focusable_widgets.index(focused_widget)
                # Move focus to the next widget, wrapping around if necessary
                next_index = (index + 1) % len(focusable_widgets)
            else:
                next_index = 0

            if focusable_widgets:
                focusable_widgets[next_index].focus = True
            return True  # Indicate that the event was handled

        return False  # Indicate that the event was not handled


class MainApp(MDApp):
    
    # App variables
    current_batch = {"batch_name": '', "ids": []}
    user_details = {
            'id_number': '',
            'firstname': '',
            'lastname': '',
            'othernames': '',
            'user_type': ''
        }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.logout_dialog = None
        # self.logout_dialog = None
        
    def set_user_details(self, id_number, firstname, lastname,othernames, user_type):
        self.user_details['id_number'] = id_number
        self.user_details['firstname'] = firstname
        self.user_details['lastname'] = lastname
        self.user_details['othernames'] = othernames
        self.user_details['user_type'] = user_type
        # print("user setting done: ", self.user_details)

    def build(self):
        # Set up the theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.2

        # Load the KV file containing the main layout
        Builder.load_file('view/main_view.kv')

        # Return the MainScreen instance, but don't add screens yet
        return MainScreen()

    def on_start(self):

        # refresh_layout()

        self.initialize_screens()
        # self.initialize_navigation_rail()

        self.animate_notice()

        # Set the initial screen to 'login_view'
        sm = self.root.ids.screen_manager
        sm.current = 'login_view'

        # Bind the event to a method to handle screen changes
        sm.bind(current=self.on_screen_change)

        # Create inspector for debugging
        inspector.create_inspector(Window, sm)

    def on_screen_change(self, instance, value):

        # Clear notice
        notice = self.root.ids.notice
        notice.text = ''

        # Get current size hints for side navigation and main screen
        side_nav = self.root.ids.side_nav
        main_window = self.root.ids.screen_manager

        if value == 'login_view':
            # Hide the side_nav by setting width to zero and opacity to zero
            side_nav.size_hint_x = 0
            side_nav.width = 0
            side_nav.opacity = 0
            main_window.size_hint_x = 1
        else:
            side_nav.opacity = 1

            # Animate back to narrow container when drawer is closed
            Animation(size_hint_x=0.065, duration=0.2).start(side_nav)  # Collapse side nav width
            Animation(size_hint_x=0.945, duration=0.2).start(main_window)

    def on_navigation_state(self, state):
        # Get current size hints for side navigation and main screen
        side_nav = self.root.ids.side_nav
        main_window = self.root.ids.main_window

        """Method to animate the container size when drawer state changes."""
        if state == 'opening_with_animation':
            # Animate to wider container when drawer is open
            Animation(size_hint_x=0.15, duration=0.2).start(side_nav)  # Expand side nav width
            Animation(size_hint_x=0.85, duration=0.2).start(main_window)  # Shrink screen manager width
        if state == 'closing_with_animation':
            # Animate back to narrow container when drawer is closed
            Animation(size_hint_x=0.065, duration=0.2).start(side_nav)  # Collapse side nav width
            Animation(size_hint_x=0.945, duration=0.2).start(
                main_window)  # Expand screen manager widthollapse rail width to

    def initialize_screens(self):
        sm = self.root.ids.screen_manager
        screens = {

            # common Screens
            'login_view': LoginScreen(name='login_view'),
            'user_profile_view': ProfileScreen(name='user_profile_view'),

            # User Screens
            'dashboard_view': DashboardScreen(name='dashboard_view'),
            'add_id_view': AddIDScreen(name='add_id_view'),
            'allocate_id_view': AllocateIDScreen(name='allocate_id_view'),
            'search_id_view': SearchIDScreen(name='search_id_view'),
            # 'sort_id_view': SortIDScreen(name='sort_id_view'),
            'contact_view': ContactScreen(name='contact_view'),
            'storage_view': StorageScreen(name='storage_view'),

            # Admin Screens
            'adminDashboard_view': AdminDashboardScreen(name='adminDashboard_view'),
            'manage_user_view': ManageUser(name='manage_user_view'),
            'config_view': ConfigScreen(name='config_view'),
            'notify_view': NotifyScreen(name='notify_view'),
            'report_view': ReportScreen(name='report_view')

        }
        for screen in screens.values():
            sm.add_widget(screen)

        nav = self.root.ids.side_nav
        nav_options = {

            # Navigation Screens
            'admin_nav': AdminNav(name='admin_nav'),
            'clerk_nav': ClerkNav(name='clerk_nav'),
        }
        for nav_option in nav_options.values():
            nav.add_widget(nav_option)

    def change_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def show_logout_dialog(self):
        if not hasattr(self, 'logout_dialog'):
            self.logout_dialog = MDDialog(
                title="Confirm Logout",
                text="Are you sure you want to logout?",
                # size_hint=(0.25, 0.25),
                size_hint=(None, None),
                size = (dp(480), dp(180)),
                buttons=[
                    MDRaisedButton(
                        text="Cancel",
                        on_release=self.close_logout_dialog
                    ),
                    MDRaisedButton(
                        text="Logout",
                        on_release=self.logout
                    )
                ]
            )
        self.logout_dialog.open()

    def close_logout_dialog(self, instance):
        self.logout_dialog.dismiss()

    def logout(self, instance):
        # Clear user data
        # current_user = CurrentUser()
        # current_user.logout()
        self.user_details = {
            'id_number': '',
            'firstname': '',
            'lastname': '',
            'othernames': '',
            'user_type': ''
        }
        self.clear_user_info()
        self.close_logout_dialog(instance)

        # Redirect to login screen
        self.root.ids.screen_manager.current = 'login_view'

    # def show_date_picker(self, text_field):
    #     # Create the date picker
    #     date_dialog = MDDatePicker(
    #         primary_color=self.theme_cls.primary_color,
    #         selector_color=self.theme_cls.accent_color,
    #         text_button_color=self.theme_cls.primary_dark,
    #     )

    #     # Set the selected date callback with text_field
    #     date_dialog.bind(on_save=lambda instance, value, date_range: self.on_save_date(text_field, value))

    #     # Open the date picker
    #     date_dialog.open()

    # def on_save_date(self, text_field, value):
    #     # Format the selected date
    #     formatted_date = value.strftime('%Y-%m-%d')
    #     text_field.text = formatted_date

    #     # If the text field is 'end_date', check if it is less than 'start_date'
    #     if text_field.id == 'end_date':
    #         start_date_str = self.ids.start_date.text
    #         if start_date_str:
    #             start_date = datetime.strptime(start_date_str, '%Y-%m-%d')  # Parse start date
    #             end_date = datetime.strptime(formatted_date, '%Y-%m-%d')  # Parse end date
                
    #             # Check if end date is less than start date
    #             if end_date < start_date:
    #                 # Set start date to end date
    #                 self.ids.start_date.text = formatted_date
                    
    #     # If the text field is 'start_date', check if it is greater than 'end_date'
    #     elif text_field.id == 'start_date':
    #         start_date_str = self.ids.start_date.text
    #         if start_date_str:
    #             start_date = datetime.strptime(start_date_str, '%Y-%m-%d')  # Parse start date
    #             end_date = datetime.strptime(formatted_date, '%Y-%m-%d')  # Parse end date
                
    #             # Check if end date is less than start date
    #             if end_date < start_date:
    #                 # Set start date to end date
    #                 self.ids.end_date.text = formatted_date

    def animate_notice(self):
        label = self.root.ids.notice
        label_size = label.font_size

        animation = Animation(
            font_size=(label_size * 1.05), duration=.6
        ) + Animation(
            font_size=label_size, duration=.6
        )

        animation.repeat = True
        animation.start(label)

    def load_user_info(self, user_data):
        # Create a new BoxLayout to hold the user avatar, name, and role
        user_box = self.root.ids.user
        user_box.clear_widgets()  # Clear any existing widgets (if any)

        avatar = MDIconButton(
            icon='account-circle',  # Or use a path to the avatar image
            user_font_size="82sp",
            pos_hint={'center_y': 0.5},
            

        )

        # Add user name and role label
        name_role_label = MDLabel(
            text=f"[b]{user_data['firstname']} {user_data['lastname']}[/b]\n[size=16sp]({user_data['user_type'].capitalize()}/ Mzuzu[/size])",
            halign="center",
            markup=True,
            valign="middle",
            # size_hint_x=None,
            # width=200,
            font_style='Subtitle1'  # Adjust font size as needed
        )
        avatar.bind(on_release = self.open_user_profile)
        user_box.add_widget(name_role_label)
        user_box.add_widget(avatar)

    def clear_user_info(self):
        user_box = self.root.ids.user
        user_box.clear_widgets()

    def open_user_profile(self, *args):
        self.change_screen('user_profile_view')

if __name__ == "__main__":
    MainApp().run()
