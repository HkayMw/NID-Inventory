from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/admin/notifyClient/notify_view.kv')


class NotifyScreen(Screen):
    def __init__(self, **kwargs):
        super(NotifyScreen, self).__init__(**kwargs)
        # self.controller = UserController()
