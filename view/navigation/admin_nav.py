from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/navigation/admin_nav.kv')


class AdminNav(Screen):
    def __init__(self, **kwargs):
        super(AdminNav, self).__init__(**kwargs)
        # self.controller = UserController()
