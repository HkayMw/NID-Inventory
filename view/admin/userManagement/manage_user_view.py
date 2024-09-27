from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/admin/userManagement/manage_user_view.kv')


class ManageUser(Screen):
    def __init__(self, **kwargs):
        super(ManageUser, self).__init__(**kwargs)
        # self.controller = UserController()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice


    def on_enter(self, *args):
        self.initialize_table()
        
        
    def initialize_table(self):
        # print("oryt!!!!!!")
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            # size_hint=(0.9, 0.9),
            # background_color_header="#008080",
            # background_color_cell="#451938",
            use_pagination=True,

            # check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("ID Number", dp(20)),
                ("Surname", dp(20)),
                ("Firstname", dp(20)),
                ("Othernames", dp(20)),
                ("Password", dp(20)),
                ("Role", dp(20)),
                # ("Sex", dp(12)),
                # ("Sorting Key", dp(20)),
                # ("Unit", dp(7)),
                # ("Status", dp(14)),
                ("Action", dp(20))
            ],
            row_data=[]
        )
        # self.background_color = [0.7, 0.7, 0.7, 1]

        # # Create a scrollable container
        # scroll_view = MDScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        # scroll_view.add_widget(self.table)

        # self.ids.lastname_field.text = "something"
        self.ids.table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.table_container.add_widget(layout)
        # print(self.root)

    # def show_menu(self):
    #     if not self.menu:
    #         menu_items = [
    #             {
    #                 "text": "Option 1",
    #                 "viewclass": "OneLineListItem",
    #                 "on_release": lambda x="Option 1": self.set_item(x),
    #             },
    #             {
    #                 "text": "Option 2",
    #                 "viewclass": "OneLineListItem",
    #                 "on_release": lambda x="Option 2": self.set_item(x),
    #             },
    #             {
    #                 "text": "Option 3",
    #                 "viewclass": "OneLineListItem",
    #                 "on_release": lambda x="Option 3": self.set_item(x),
    #             },
    #         ]
    #         self.menu = MDDropdownMenu(items=menu_items, width_mult=4)
    #     self.menu.open()