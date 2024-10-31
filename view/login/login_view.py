# screens/login/login_view.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from Assets.qr_code import QRCode


# Builder.load_file('view/UI.kv')
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
                self.app.set_user_details(
                    id_number=user[0],
                    firstname=user[1],
                    lastname=user[2],
                    othernames=user[3],
                    user_type=user[5]
                )
                
                user_data = self.app.user_details
                
                if user_data['user_type'].lower() == 'admin':
                    
                    self.app.root.ids.side_nav.current = 'admin_nav'
                    items = self.app.root.ids.side_nav.get_screen('admin_nav').ids.navigation_rail.children[0].children[0].children
                    for item in items:
                        item.active = False
                        
                    self.app.root.ids.side_nav.get_screen('admin_nav').ids.dashboard.trigger_action(0)
                    self.app.change_screen('adminDashboard_view')
                    
                else:
                    
                    self.app.root.ids.side_nav.current = 'clerk_nav'
                    items = self.app.root.ids.side_nav.get_screen('clerk_nav').ids.navigation_rail.children[0].children[0].children
                    for item in items:
                        item.active = False
                        
                    self.app.root.ids.side_nav.get_screen('clerk_nav').ids.dashboard.trigger_action(0)
                    self.app.change_screen('dashboard_view')
                    
                self.app.load_user_info(user_data)
                    
                
                # Unbind only if the event is bound
                try:
                    self.app.root.ids.side_nav.get_screen('clerk_nav').ids.dashboard.unbind(on_release=self.app.change_screen)
                except Exception as e:
                    print(f"Error unbinding clerk nav: {e}")
                
                try:
                    self.app.root.ids.side_nav.get_screen('admin_nav').ids.dashboard.unbind(on_release=self.app.change_screen)
                except Exception as e:
                    print(f"Error unbinding clerk nav: {e}")

                # Bind the events after unbinding
                self.app.root.ids.side_nav.get_screen('clerk_nav').ids.dashboard.bind(on_release=lambda x: self.app.change_screen('dashboard_view'))
                self.app.root.ids.side_nav.get_screen('admin_nav').ids.dashboard.bind(on_release=lambda x: self.app.change_screen('adminDashboard_view'))

                
                # Clear credentials
                self.ids.id_no_field.text = ""
                self.ids.password_field.text = ""
                
            else:
                
                notice.text = f"{message}"
