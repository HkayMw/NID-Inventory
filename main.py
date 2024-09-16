from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.boxlayout import BoxLayout

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

        # Load the KV file containing the main layout
        Builder.load_file('view/main_view.kv')

        # Return the MainScreen instance, but don't add screens yet
        return MainScreen()

    def on_start(self):

        # Initialize screens
        self.initialize_screens()

        # Set the initial screen to 'search_id_view'
        sm = self.root.ids.screen_manager
        sm.current = 'search_id_view'

        # Create inspector for debugging
        inspector.create_inspector(Window, sm)

    def initialize_screens(self):
        sm = self.root.ids.screen_manager
        # sm = self.root.ids

        # Creating instances of screens
        login_screen = LoginScreen(name='login_view')
        search_id_screen = SearchIDScreen(name='search_id_view')
        add_id_screen = AddIDScreen(name='add_id_view')
        sort_id_screen = SortIDScreen(name='sort_id_view')
        contact_screen = ContactScreen(name='contact_view')

        # Adding screens to MainScreen's ScreenManager
        sm.add_widget(login_screen)
        sm.add_widget(search_id_screen)
        sm.add_widget(add_id_screen)
        sm.add_widget(sort_id_screen)
        sm.add_widget(contact_screen)

    # def callback_function(self):
    #     # Example callback for toolbar button actions
    #     print("Toolbar button pressed!")



    

if __name__ == "__main__":
    MainApp().run()
