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
        self.app = MDApp.get_running_app()

    def validate_user(self):
        id_number = self.ids.id_no_field
        password = self.ids.password_field
        
        # Clear notice
        notice = self.app.root.ids.notice
        notice.text = ''

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
                    notice.text = f"QR Code error: {message}"
                    return  # Exit the method to avoid further processing
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
                user_data = current_user.get_user_details()
                # app.update_navigation(current_user.get_user_details())
                
                # self.parent.parent.current = 'add_id_view'
                # self.manager.current = "search_id_view"
                # print(current_user.user_details)
                if user_data['user_type'] == 'admin':
                    
                    self.app.root.ids.side_nav.current = 'admin_nav'
                    self.app.root.ids.side_nav.get_screen('admin_nav').ids.navigation_rail.current_selected_item = 0
                    self.app.change_screen('adminDashboard_view')
                    
                    # print(f"logged in as {current_user.user_details['user_type']}")
                
                else:
                    
                    self.app.root.ids.side_nav.current = 'clerk_nav'
                    self.app.root.ids.side_nav.get_screen('clerk_nav').ids.navigation_rail.current_selected_item = 1
                    self.app.change_screen('dashboard_view')
                    
                    
                    # print(f"logged in as {current_user.user_details['user_type']}")
                
                self.app.load_user_info(user_data)
                    
                self.app.root.ids.side_nav.get_screen('clerk_nav').ids.dashboard.on_release = lambda: self.app.change_screen('dashboard_view')
                self.app.root.ids.side_nav.get_screen('admin_nav').ids.dashboard.on_release = lambda: self.app.change_screen('adminDashboard_view')
                
                # Clear credentials
                self.ids.id_no_field.text = ""
                self.ids.password_field.text = ""
                # print(app.root.ids.side_nav.get_screen('admin_nav').ids.navigation_rail.current_selected_item)
                
            else:
                
                notice.text = f"{message}"
