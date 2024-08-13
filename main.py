# main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from view.login_view import LoginScreen
from view.home_view import HomeScreen
from view.adminDashboard_view import AdminDashboardScreen

class MainScreen(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file('view/main_view.kv')
        sm = MainScreen()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(HomeScreen(name='home_screen'))

        sm.current = 'login_view'
        return sm

if __name__ == "__main__":
    MainApp().run()
