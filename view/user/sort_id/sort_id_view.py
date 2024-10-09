from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from controller.user_controller import UserController
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user/sort_id/sort_id_view.kv')


class SortIDScreen(Screen):
    def __init__(self, **kwargs):
        super(SortIDScreen, self).__init__(**kwargs)
        # self.controller = UserController()
        
        self.data_tables = None
        self.app = MDApp.get_running_app()
        
        # Clear notice
        self.notice = self.app.root.ids.notice
        # self.notice.text = ''
        
    def on_enter(self, *args):
        self.initialize_sorting_guide_table()
        self.initialize_allocate_storage_table()
        self.initialize_generate_sorting_key_table()
        # for tab in self.ids.tabs.get_tab_list():
        #     tab.disabled = True
        # def disable_tab_touch(instance, touch):
        #     return True
        
        # self.ids.tabs.on_touch_down = disable_tab_touch
        
    def initialize_sorting_guide_table(self):
        # print("oryt!!!!!!")
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            # size_hint=(0.9, 0.9),
            # background_color_header="#008080",
            # background_color_cell="#451938",
            use_pagination=True,

            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Sorting Key", dp(40)),
                ("ID Count", dp(40)),
                ("Storage Unit", dp(40)),
                # ("D_O_B", dp(20)),
                # ("ID Number", dp(20)),
                # ("Issue Date", dp(20)),
                # ("Sex", dp(20)),
                # ("Sorting Key", dp(20)),
                # ("Unit", dp(20)),
                # ("Status", dp(20)),
                # ("Action", dp(20)),
            ],
            row_data=[]
        )
        # self.background_color = [0.7, 0.7, 0.7, 1]

        # # Create a scrollable container
        # scroll_view = MDScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        # scroll_view.add_widget(self.table)

        # self.ids.lastname_field.text = "something"
        self.ids.sorting_guide_table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.sorting_guide_table_container.add_widget(layout)
        # print(self.root)
        
        
    def initialize_allocate_storage_table(self):
        # print("oryt!!!!!!")
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            # size_hint=(0.9, 0.9),
            # background_color_header="#008080",
            # background_color_cell="#451938",
            use_pagination=True,

            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Sorting Key", dp(40)),
                ("ID Count", dp(40)),
                ("Assign Storage Unit", dp(40)),
                # ("D_O_B", dp(20)),
                # ("ID Number", dp(20)),
                # ("Issue Date", dp(20)),
                # ("Sex", dp(20)),
                # ("Sorting Key", dp(20)),
                # ("Unit", dp(20)),
                # ("Status", dp(20)),
                # ("Action", dp(20)),
            ],
            row_data=[]
        )
        # self.background_color = [0.7, 0.7, 0.7, 1]

        # # Create a scrollable container
        # scroll_view = MDScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        # scroll_view.add_widget(self.table)

        # self.ids.lastname_field.text = "something"
        self.ids.allocate_storage_table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.allocate_storage_table_container.add_widget(layout)
        # print(self.root)
        
    def initialize_generate_sorting_key_table(self):
        # print("oryt!!!!!!")
        # Initialize the table with default headers and an empty state
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            # size_hint=(0.9, 0.9),
            # background_color_header="#008080",
            # background_color_cell="#451938",
            use_pagination=True,

            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Sorting Key", dp(50)),
                ("ID Count", dp(50)),
                # ("Assign Storage Unit", dp(40)),
                # ("D_O_B", dp(20)),
                # ("ID Number", dp(20)),
                # ("Issue Date", dp(20)),
                # ("Sex", dp(20)),
                # ("Sorting Key", dp(20)),
                # ("Unit", dp(20)),
                # ("Status", dp(20)),
                # ("Action", dp(20)),
            ],
            row_data=[]
        )
        # self.background_color = [0.7, 0.7, 0.7, 1]

        # # Create a scrollable container
        # scroll_view = MDScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        # scroll_view.add_widget(self.table)

        # self.ids.lastname_field.text = "something"
        self.ids.generate_sorting_key_table_container.clear_widgets()
        layout.add_widget(self.data_tables)
        self.ids.generate_sorting_key_table_container.add_widget(layout)
        # print(self.root)


class Tab(BoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass
    
    