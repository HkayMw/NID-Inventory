from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/userManagement/manage_user_view.kv')


class ManageUser(Screen):
    def __init__(self, **kwargs):
        super(ManageUser, self).__init__(**kwargs)
        # self.controller = UserController()
