# controller/controller.py

class Controller:
    def __init__(self, model):
        self.model = model
        

    def create_record(self, table, data):
        self.model.create(data)

    def read_records(self, table, where_clause=None):
        data = self.model.read(where_clause)
        self.view.display_data(data)

    def update_record(self, table, data, where_clause):
        self.model.update(data, where_clause)

    def delete_record(self, table, where_clause):
        self.model.delete(where_clause)