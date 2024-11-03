from kivy.config import Config

# Set the default window size
default_width = 1200
default_height = 600

# Config.set('graphics', 'width', str(default_width))
# Config.set('graphics', 'height', str(default_height))


from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import NoTransition, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import StringProperty

from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.segmentedcontrol import MDSegmentedControl
from kivymd.uix.scrollview import MDScrollView
import kivymd

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
from view.sync.sync_view import SyncScreen

import subprocess

import psutil
import threading
import time
import socket
import os
import sys
# Maximize the window size on startup
# Window.size = (Window.width, Window.height)  # Start with the full size of the window

# Alternatively, for a fullscreen experience
# Window.fullscreen = True

# Maximize the window on start
Window.maximize()
Window.set_icon("Assets/icon.png")
        
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
    
    network_status = StringProperty('disconnected')  # Use StringProperty for live updates
    internet_status = StringProperty('disconnected')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set the transition
        self.ids.screen_manager.transition = NoTransition()
        # Bind the on_key_down event
        Window.bind(on_key_down=self.on_key_down)
        self.check_network_status()  # Initial check
        threading.Thread(target=self.monitor_network, daemon=True).start()  # Start monitoring
        
    def check_network_status(self):
        # Check if connected to any network
        is_connected = any(psutil.net_if_stats()[iface].isup for iface in psutil.net_if_stats())

        # Update network_status
        self.network_status = 'connected' if is_connected else 'disconnected'
        
        # Check internet connectivity
        self.check_internet_connectivity()

    def check_internet_connectivity(self):
        # Attempt to connect to Google's DNS server to check for internet connectivity
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.internet_status = 'connected'
        except (socket.timeout, OSError):
            self.internet_status = 'disconnected'

    def monitor_network(self):
        while True:
            self.check_network_status()
            time.sleep(5)  # Check every 5 seconds

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
    network_status = StringProperty('disconnected')  # Use StringProperty for live updates
    internet_status = StringProperty('disconnected')
    
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
        # Set the app icon
        # self.network_status = 'disconnected'
        # self.internet_status = 'disconnected'
        
    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
        


    # Method to center the window on the screen
    def center_window(self, *args):
        # Set window's top-left corner to the screen's top-left corner
        Window.left = 0
        Window.top = 30
        # print
        
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
        Builder.load_file(self.resource_path('view/main_view.kv'))

        # Return the MainScreen instance, but don't add screens yet
        return MainScreen()

    def on_start(self):
        
        

        # refresh_layout()
        # Bind the window size change event to the center_window method
        Window.bind(size=self.center_window)

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
            'sync_view': SyncScreen(name='sync_view'),

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
            'clerk_nav': ClerkNav(name='clerk_nav'),
            'admin_nav': AdminNav(name='admin_nav'),
        }
        for nav_option in nav_options.values():
            nav.add_widget(nav_option)

    def change_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def show_logout_dialog(self, *args):
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
        avatar1 = MDIconButton(
            icon='logout',  # Or use a path to the avatar image
            user_font_size="82sp",
            pos_hint={'center_y': 0.5},
        )
        avatar2 = MDIconButton(
            icon='sync',  # Or use a path to the avatar image
            user_font_size="92sp",
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
        avatar1.bind(on_release = self.show_logout_dialog)
        avatar2.bind(on_release = lambda x: self.change_screen('sync_view'))
        user_box.add_widget(avatar2)
        user_box.add_widget(name_role_label)
        user_box.add_widget(avatar)
        user_box.add_widget(avatar1)

    def clear_user_info(self):
        user_box = self.root.ids.user
        user_box.clear_widgets()

    def open_user_profile(self, *args):
        self.change_screen('user_profile_view')

if __name__ == "__main__":
    MainApp().run()
