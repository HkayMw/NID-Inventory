from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

class DataTableApp(MDApp):
    # print(self.ids)
    def build(self):
        layout = BoxLayout(orientation='vertical')

        data_tables = MDDataTable(
            
            size_hint=(1, 0.7),
            use_pagination=True,
            column_data=[
                ("No", dp(30)),
                ("Name", dp(30)),
                ("Email", dp(60)),
            ],
            row_data=[
                (1, "John Doe", "johndoe@example.com"),
                (2, "Jane Smith", "janesmith@example.com"),
                # ... more rows
            ],
        )

        data_tables.id='table'
        layout.add_widget(data_tables)
        return layout

DataTableApp().run()
