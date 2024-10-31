from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/user_profile/user_profile_view.kv')


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.user_controller = UserController()
        self.app = MDApp.get_running_app()
        self.notice = self.app.root.ids.notice
        
        
    def on_enter(self, *args):
        self.ids.current_password.text = ''
        self.ids.new_password.text = ''
        self.ids.new_password1.text = ''
        
        items = self.app.root.ids.side_nav.get_screen('admin_nav').ids.navigation_rail.children[0].children[0].children
        for item in items:
            item.active = False
            
        items = self.app.root.ids.side_nav.get_screen('clerk_nav').ids.navigation_rail.children[0].children[0].children
        for item in items:
            item.active = False
        
        
        if self.app.user_details['othernames']:
            self.ids.full_name.text = self.app.user_details['firstname'] + " " + self.app.user_details['othernames'] + " " + self.app.user_details['lastname']
        else:
            self.ids.full_name.text = self.app.user_details['firstname'] + " " + self.app.user_details['lastname']
        self.ids.id_number.text = self.app.user_details['id_number']
        self.ids.role.text = self.app.user_details['user_type']
        return super().on_enter(*args)
    
    def change_password(self):
        current_password = self.ids.current_password.text
        new_password = self.ids.new_password.text
        new_password1 = self.ids.new_password1.text
        
        if (not current_password) or (not new_password) or (not new_password1):
            self.notice.text = 'All fields are required to change password'
            return
        if new_password == new_password1:
            password = new_password
        else:
            self.notice.text = 'New Passwords dont match, please check'
            return
        
        id_number = self.app.user_details['id_number']
        
        success, message, user = self.user_controller.validate_user(id_number, current_password)
        
        if success:
            # clear password fields
            self.ids.current_password.text = ''
            self.ids.new_password.text = ''
            self.ids.new_password1.text = ''
            
            user_data = {'id_number': id_number, 'password': password}
            success, message, user = self.user_controller.update_user(user_data)
            
            # print(success, " ", message, " ", user)
            if success:
                self.notice.text = 'Password Updated Successfully'
            else:
                self.notice.text = 'Something went wrong updating password'
                return 
        else:
            self.notice.text = 'Wrong current password provided'
            return 
