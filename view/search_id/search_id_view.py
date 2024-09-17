from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout

# from controller.user_controller import UserController
from controller.id_controller import IdController
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window

# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.datatables import MDDataTable
# from kivy.metrics import dp



# Builder.load_file('view/UI.kv')
Builder.load_file('view/search_id/search_id_view.kv')

class SearchIDScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None
        self.controller = IdController()

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
                ("Surname", dp(20)),
                ("Firstname", dp(20)),
                ("Othernames", dp(20)),
                ("D_O_B", dp(20)),
                ("ID Number", dp(17)),
                ("Issue Date", dp(17)),
                ("Sex", dp(12)),
                ("Sorting Key", dp(20)),
                ("Unit", dp(7)),
                ("Status", dp(14)),
                ("Action", dp(11)),
            ],
            row_data=[],
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

    

    def search_id(self, search_type):
        
        # Clear notice
        notice = self.parent.parent.parent.ids.notice
        notice.text = ''
        # print("some notice: ",notice.text)
        
            # print(qr_code)
            # return 
        
        search_results = []
        if search_type == 'id':
            id_number = self.ids.id_no_field.text
            
            success, message, search_results = self.controller.search_id(search_type='id', id_number=id_number)
            if not success:
                notice.theme_text_color = "Error"
                notice.text = message
            else:
                notice.text = message
            
            #clear ID Number input field    
            self.ids.id_no_field.text = ''

        elif search_type == 'name':
            firstname = self.ids.firstname_field.text
            lastname = self.ids.lastname_field.text
            
            
            success, message, search_results = self.controller.search_id(search_type='name', firstname=firstname, lastname=lastname)
            if not success:
                # self.parent.parent.parent.ids.notice.theme_text_color = "Error"
                notice.theme_text_color = "Error"
                notice.text = message
            else:
                #todo: change to green
                notice.text = message
                
            self.ids.firstname_field.text = ''
            self.ids.lastname_field.text = ''

        elif search_type == 'qr_code':
            qr_code = self.ids.qr_code.text
            success, message, search_results = self.controller.search_id(search_type='qr_code', qr_code=qr_code)
            if not success:
                notice.theme_text_color = "Error"
                notice.text = message
            self.ids.qr_code.text = ''
        
        # Update table with search results
        if search_results:
            # print(len(search_results))
            self.update_row_data(self.data_tables, search_results)
        else:
            # Clear the current row data
            self.data_tables.row_data =[]

        
        
        
        # search_results = self.controller.search_ids()  # Assuming this method returns a list of row data

        # self.update_row_data(self.data_tables, search_results)
        
    def update_row_data(self, instance_data_table, search_results):
        """
        Updates the row data of the given data table instance.

        :param instance_data_table: The instance of the data table to update.
        :param search_results: Raw data from search results.
        """
        try:
            # Transform the search results to match the datatable format
            data = self.transform_data_for_datatable(search_results)
            
            # Update the table with new row data
            instance_data_table.row_data = data

            # print("Row data updated successfully.")
        
        except AttributeError as e:
            print(f"Error: {e}. Make sure instance_data_table is a valid data table with row_data attribute.", __name__)
        except ValueError as e:
            print(f"Error: {e}.")

        
        except Exception as e:
            print(f"Error: {e}")


    def transform_data_for_datatable(self, search_results):
        """
        Transforms search results into the format required by MDDataTable.

        :param search_results: A list of dictionaries containing search results.
        :return: A list of lists containing only the necessary columns for MDDataTable.
        """
        # Define the columns to include in the datatable
        required_columns = ['lastname', 'firstname', 'othernames', 'd_o_b', 'id_number', 'issue_date', 'gender', 'sorting_key', 'Unit', 'status']
        
        # Transform the data
        transformed_data = []
        for result in search_results:
            row = [result.get(col, '').capitalize() for col in required_columns]
            row.append(f'')
            transformed_data.append(row)
        
        return transformed_data    
        