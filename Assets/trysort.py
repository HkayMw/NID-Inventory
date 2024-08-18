from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

KV = '''
MDScreen:

    MDDataTable:
        id: data_table
        pos_hint: {"center_y": 0.5, "center_x": 0.5}
        size_hint: (0.9, 0.6)
        use_pagination: True
'''

class ExampleApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        data_table = self.root.ids.data_table
        data_table.column_data = [
            ("No.", dp(30)),
            ("Food", dp(30)),
            ("Calories", dp(30)),
            ("Type", dp(30)),
        ]
        data_table.row_data = [
            (str(i), f"Food {i}", str(i * 100), "Fruit" if i % 2 == 0 else "Vegetable")
            for i in range(1, 101)
        ]

if __name__ == "__main__":
    ExampleApp().run()
