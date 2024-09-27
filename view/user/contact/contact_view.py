from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
# from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/contact/contact_view.kv')


class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)
        # self.controller = UserController()
        self.data_tables = None
        # self.controller = IdController()
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        # self.notice.text = ''

    def on_enter(self, *args):
        self.initialize_table()
        # print(self.parent.current)
        
    # def on_kv_post(self, base_widget):
    #     print("Table container size:", self.ids.table_container.size)
    #     print("Table container pos:", self.ids.table_container.pos)

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
                ("ID Number", dp(40)),
                ("Phone Number", dp(40)),
                # ("Firstname", dp(20)),
                # ("Othernames", dp(20)),
                # ("D_O_B", dp(20)),
                # ("Issue Date", dp(20)),
                # ("Sex", dp(20)),
                # ("Sorting Key", dp(20)),
                # ("Unit", dp(20)),
                # ("Status", dp(20)),
                ("Action", dp(40)),
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
