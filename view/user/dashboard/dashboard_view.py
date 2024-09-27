
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_file('view/user/dashboard/dashboard_view.kv')

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
