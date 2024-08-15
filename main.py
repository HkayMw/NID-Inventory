# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from view.login_view import LoginScreen
from view.search_id_view import SearchIDScreen
from view.add_id_view import AddIDScreen
from view.adminDashboard_view import AdminDashboardScreen
from kivy.config import Config
from kivy.core.window import Window


# Set the default window size
default_width = 800
default_height = 600
Config.set('graphics', 'width', str(default_width))
Config.set('graphics', 'height', str(default_height))

# Set the minimum size to be the same as the default size
Window.minimum_width = default_width
Window.minimum_height = default_height

# from kivy.uix.debug import Debug

class MainScreen(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file('view/main_view.kv')
        sm = MainScreen(transition=NoTransition())
        # sm.add_widget(LoginScreen(name='login_view'))
        # sm.add_widget(AddIDScreen(name='add_id_view'))

        sm.current = 'search_id_view'
        
        # # Bind the on_key_down event for tab navigation
        # Window.bind(on_key_down=login_screen.on_key_down)
        
        return sm
    
    

if __name__ == "__main__":
    MainApp().run()
