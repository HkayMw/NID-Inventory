from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
# from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.navigationrail import MDNavigationRailItem


# Importing navigation views
from view.navigation.clerk_nav import ClerkNav
from view.navigation.admin_nav import AdminNav


# Importing custom screens
from view.login.login_view import LoginScreen
from view.search_id.search_id_view import SearchIDScreen
from view.add_id.add_id_view import AddIDScreen
from view.sort_id.sort_id_view import SortIDScreen
from view.contact.contact_view import ContactScreen
from view.adminDashboard.adminDashboard_view import AdminDashboardScreen

# Set the default window size
default_width = 800
default_height = 600
Config.set('graphics', 'width', str(default_width))
Config.set('graphics', 'height', str(default_height))

# Set the minimum size to be the same as the default size
Window.minimum_width = default_width
Window.minimum_height = default_height

# Define MainScreen as a ScreenManager
class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the transition
        self.ids.screen_manager.transition = NoTransition()
        # Bind the on_key_down event
        Window.bind(on_key_down=self.on_key_down)
        
        # Bind the drawer's state change event
        # nav_drawer = .ids.nav_drawer
        # nav_drawer.bind(state=main_container.on_navigation_state)
        
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

            
            focusable_widgets[next_index].focus = True
            return True  # Indicate that the event was handled

        return False  # Indicate that the event was not handled
    
    
class MainApp(MDApp):
    def build(self):
        # Set up the theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"

        # Load the KV file containing the main layout
        Builder.load_file('view/main_view.kv')

        # Return the MainScreen instance, but don't add screens yet
        return MainScreen()

    def on_start(self):
        
        self.initialize_screens()
        # self.initialize_navigation_rail()

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
        
        # Get the side_nav and screen_manager references
        side_nav = self.root.ids.side_nav
        screen_manager = self.root.ids.screen_manager

        if value == 'login_view':
            # Hide the side_nav by setting width to zero and opacity to zero
            side_nav.size_hint_x = 0
            side_nav.width = 0
            side_nav.opacity = 0
            screen_manager.size_hint_x = 1
        else:
            # Restore the side_nav and screen_manager to their original state
            # side_nav.size_hint_x = 0.07
            # side_nav.width = None  # This allows size_hint_x to take effect
            side_nav.opacity = 1
            # screen_manager.size_hint_x = 0.93
            
            # Animate back to narrow container when drawer is closed
            Animation(size_hint_x=0.07, duration=0.2).start(side_nav)  # Collapse side nav width
            Animation(size_hint_x=0.93, duration=0.2).start(screen_manager)  
            
    def on_navigation_state(self, state):
        # Get current size hints for side navigation and screen manager
        side_nav = self.root.ids.side_nav
        screen_manager = self.root.ids.screen_manager
        
        # side_nav_width = side_nav.size_hint_x
        # screen_manager_width = screen_manager.size_hint_x
        print(f'state: {state}')

        """Method to animate the container size when drawer state changes."""
        if state == 'opening_with_animation':
            # Animate to wider container when drawer is open
            Animation(size_hint_x=0.15, duration=0.2).start(side_nav)  # Expand side nav width
            Animation(size_hint_x=0.85, duration=0.2).start(screen_manager)  # Shrink screen manager width
        if state == 'closing_with_animation':
            # Animate back to narrow container when drawer is closed
            Animation(size_hint_x=0.07, duration=0.2).start(side_nav)  # Collapse side nav width
            Animation(size_hint_x=0.93, duration=0.2).start(screen_manager)  # Expand screen manager widthollapse rail width to 

    def initialize_screens(self):
        sm = self.root.ids.screen_manager
        screens = {
            'login_view': LoginScreen(name='login_view'),
            'search_id_view': SearchIDScreen(name='search_id_view'),
            'add_id_view': AddIDScreen(name='add_id_view'),
            'sort_id_view': SortIDScreen(name='sort_id_view'),
            'contact_view': ContactScreen(name='contact_view')
        }
        for screen in screens.values():
            sm.add_widget(screen)
            
        nav = self.root.ids.side_nav
        nav_options = {
            'clerk_nav': ClerkNav(name='clerk_nav'),
            'admin_nav': AdminNav(name='admin_nav')
        }
        for nav_option in nav_options.values():
            nav.add_widget(nav_option)
            
            
    
            
    # def initialize_navigation_rail(self):
    #     nav_rail = self.root.ids.side_nav
    #     items = [
    #         ('Add IDs', 'plus', 'add_id_view'),
    #         ('Search IDs', 'magnify', 'search_id_view'),
    #         ('Sort IDs', 'sort', 'sort_id_view'),
    #         ('Contacts', 'contacts', 'contact_view'),
    #         ('Logout', 'logout', 'login_view')
    #     ]
    #     for text, icon, screen_name in items:
    #         item = MDNavigationRailItem(
    #             text=text,
    #             icon=icon,
    #             on_release=lambda x, sn=screen_name: self.change_screen(sn)
    #         )
    #         nav_rail.add_widget(item)
            
            
    # def update_navigation(self, user = {'user_type' : 'guest'}):
    #     print(self.root.ids)
    #     if user['user_type'] == 'admin':
    #         pass
    #     else:
    #         # Clear existing items
    #         # self.root.ids.rail_items.clear_widgets()
    #         # self.root.ids.drawer_items.clear_widgets()

    #         # Example items for the rail
    #         items = [
    #             {"text": "Add IDs", "icon": "plus", "screen": "add_id_view"},
    #             {"text": "Search IDs", "icon": "magnify", "screen": "search_id_view"},
    #             {"text": "Sort IDs", "icon": "sort", "screen": "sort_id_view"},
    #             {"text": "Contacts", "icon": "contacts", "screen": "contact_view"},
    #             {"text": "Logout", "icon": "logout", "screen": "login_view"},
    #         ]

    #         # Update Navigation Rail
    #         for item in items:
    #             rail_item = MDNavigationRailItem(text=item['text'], icon=item['icon'])
    #             rail_item.bind(on_release=lambda x=item['screen']: self.change_screen(x))
    #             self.root.ids.rail_items.add_widget(rail_item)

    #         # Update Navigation Drawer
    #         for item in items:
    #             drawer_item = OneLineIconListItem(text=item['text'])
    #             drawer_item.add_widget(IconLeftWidget(icon=item['icon']))
    #             drawer_item.bind(on_release=lambda x=item['screen']: self.change_screen(x))
    #             self.root.ids.drawer_items.add_widget(drawer_item)
            
    def change_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
        # self.root.ids.nav_drawer.set_state("close")

    # def callback_function(self):
    #     # Example callback for toolbar button actions
    #     print("Toolbar button pressed!")
    
    def switch_screen(
        self, instance_navigation_rail, instance_navigation_rail_item
    ):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''

        self.root.ids.screen_manager.current = (
            instance_navigation_rail_item.icon.split("-")[1].lower()
        )



    

if __name__ == "__main__":
    MainApp().run()
