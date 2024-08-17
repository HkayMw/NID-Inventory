from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window

# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.datatables import MDDataTable
# from kivy.metrics import dp


# Builder.load_file('view/UI.kv')
Builder.load_file('view/search_id/search_id_view.kv')


class SearchIDScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchIDScreen, self).__init__(**kwargs)
        self.controller = UserController()

    #     self.create_datatable()
    #     print("layout IDs: ", self.ids)

    # def create_datatable(self):
    #     # Create the MDDataTable
    #     data_table = MDDataTable(
    #         size_hint_y=None,
    #         height=Window.height - 100,  # Adjust the height as needed
    #         column_data=[
    #             ("ID", dp(30)),
    #             ("Name", dp(50)),
    #             ("Date of Birth", dp(50)),
    #             ("Status", dp(30))
    #         ]
    #     )

    # Add the MDDataTable to the placeholder in the KV file
    # table_container = self.ids.table_container
    # table_container.clear_widgets()  # Optional: clear existing widgets
    # table_container.add_widget(data_table)
