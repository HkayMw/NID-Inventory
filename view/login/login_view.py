# screens/login/login_view.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from model.current_user import CurrentUser
from kivy.core.window import Window
from Assets.qr_code import QRCode
from kivy.uix.boxlayout import BoxLayout


# # Builder.load_file('view/UI.kv')
Builder.load_file('view/login/login_view.kv')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.controller = UserController()
        # Window.bind(on_key_down=self.on_key_down)  # Bind the on_key_down event

    def validate_user(self):
        id_number = self.ids.id_no_field
        password = self.ids.password_field
        # notice = self.ids.notice# Clear notice
        notice = self.parent.parent.parent.ids.notice
        # notice.text = ''

        # print(id_no + " " + password)

        if id_number.text == "" or password.text == "":
            notice.text = f"id_no and/ or password required"
        else:
            
            # Check if qr code is provided
            if '~' in id_number.text:
                self.qr_code = QRCode(id_number.text) 
                success, message, id = self.qr_code.process()
                
                if success:
                    try:
                        id_number = id['id_number']
                        
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print(message)
            else:
                id_number = id_number.text
            
            valid, message, user = self.controller.validate_user(id_number.upper(), password.text)
            if valid:
                # user = message
                # notice.text = f"[color=#00ff00]{message}, {user}[/color]"
                # print(user)
                current_user = CurrentUser()
                # print(user)
                current_user.set_user_details(
                    id_number=user[0],
                    firstname=user[1],
                    lastname=user[2],
                    othernames=user[3],
                    user_type=user[5]
                )
                
                # print(current_user.get_user_details())
                app = MDApp.get_running_app()
                # app.update_navigation(current_user.get_user_details())

                # self.parent.parent.current = 'add_id_view'
                # self.manager.current = "search_id_view"
                app.root.ids.screen_manager.current = 'search_id_view'
                app.roo.ids.side_nav.current = 'clerk_nav'
            else:
                app = MDApp.get_running_app()
                # app.update_navigation()
                
                notice.text = f"{message}"
