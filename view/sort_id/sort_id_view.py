from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window

# Builder.load_file('view/UI.kv')
Builder.load_file('view/sort_id/sort_id_view.kv')


class SortIDScreen(Screen):
    def __init__(self, **kwargs):
        super(SortIDScreen, self).__init__(**kwargs)
        self.controller = UserController()
