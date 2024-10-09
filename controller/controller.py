# controller/controller.py

class Controller:
    def __init__(self, model):
        self.model = model

    def custom_query(self, data):
        return self.model.custom_query(data)
    
    def create(self, data):
        return self.model.create(data)

    def read(self, where_clause=None, params=None):
        return self.model.read(where_clause, params)

    def update(self, data, where_clause, params=None):
        return self.model.update(data, where_clause, params)

    def delete(self, where_clause, params=None):
        return self.model.delete(where_clause, params)
