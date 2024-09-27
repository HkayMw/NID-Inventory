
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('view/admin/adminDashboard/adminDashboard_view.kv')

class AdminDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminDashboardScreen, self).__init__(**kwargs)
        