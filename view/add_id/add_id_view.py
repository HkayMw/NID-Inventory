from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window


# Builder.load_file('view/UI.kv')
Builder.load_file('view/add_id_view.kv')



class AddIDScreen(Screen):
    def __init__(self, **kwargs):
        super(AddIDScreen, self).__init__(**kwargs)
        self.controller = UserController()