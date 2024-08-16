from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window


# Builder.load_file('view/UI.kv')
Builder.load_file('view/contact_view.kv')



class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        self.controller = UserController()