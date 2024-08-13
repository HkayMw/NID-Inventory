# model/users_model.py

from model.model import Model


class UsersModel(Model):
    def __init__(self) -> None:
        super().__init__()

    def create_table(self):
        self.execute_query('''CREATE TABLE IF NOT EXISTS users
               (id_no TEXT(8) PRIMARY KEY UNIQUE,
               first_name TEXT,
               last_name TEXT,
               other_names TEXT,
               password TEXT,
               user_type TEXT,
               created_on DATETIME,
               updated_on DATETIME)''')

    def validate_user(self, id_no, password):
        return self.fetch_one('SELECT * FROM users WHERE id_no=? AND password=?', id_no, password)

    def add_user(self):
        pass
