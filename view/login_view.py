#screens/login_view.py

from kivy.uix.screenmanager import Screen
from controller.users_controller import UsersController
from kivy.lang import Builder


Builder.load_file('view/UI.kv')
# Builder.load_file('view/login_view.kv')



class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.controller = UsersController()
    

    def validate_user(self):
        id_no = self.ids.id_no_field
        password = self.ids.password_field
        notice = self.ids.notice

        # print(id_no + " " + password)

        if id_no.text == "" or password.text == "":
            notice.text = "[color=#ff0000]id_no and/ or password required[/color]"
        else:
            valid, message = self.controller.validate_user(id_no.text.upper(), password.text)
            if valid:
                notice.text = f"[color=#00ff00]{message}[/color]"
                self.manager.current = 'login_view'
            else:
                notice.text = f"[color=#ff0000]{message}[/color]"

# class LoginApp(App):
#     def build(self):
#         return LoginWindow()


# if __name__ == "__main__":
#     login = LoginApp()
#     login.run()
