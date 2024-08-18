# screens/login/login_view.py

from kivy.uix.screenmanager import Screen
from controller.user_controller import UserController
from kivy.lang import Builder
from model.current_user import CurrentUser
from kivy.core.window import Window

# Builder.load_file('view/UI.kv')
Builder.load_file('view/login/login_view.kv')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.controller = UserController()
        Window.bind(on_key_down=self.on_key_down)  # Bind the on_key_down event

    def validate_user(self):
        id_no = self.ids.id_no_field
        password = self.ids.password_field
        notice = self.ids.notice

        # print(id_no + " " + password)

        if id_no.text == "" or password.text == "":
            notice.text = f"[color=#ff0000]id_no and/ or password required[/color]"
        else:
            valid, message, user = self.controller.validate_user(id_no.text.upper(), password.text)
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

                self.manager.current = 'add_id_view'
            else:
                notice.text = f"[color=#ff0000]{message}[/color]"

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # print(f"Keycode: {keycode}")
        if keycode == 43:
            # Collect all focusable widgets
            focusable_widgets = []
            for widget in self.walk(restrict=True):
                if hasattr(widget, 'focus') and widget.is_focusable:
                    focusable_widgets.append(widget)

            # for x in focusable_widgets: print(x.)
            # Find the currently focused widget
            focused_widget = next((w for w in focusable_widgets if w.focus), None)
            # print(focused_widget)
            if focused_widget:
                # Find the index of the focused widget
                index = focusable_widgets.index(focused_widget)
                # Move focus to the next widget, wrapping around if necessary
                next_index = (index + 1) % len(focusable_widgets)
            else:
                next_index = 0
            focusable_widgets[next_index].focus = True
            return True  # Indicate that the event was handled

        return False  # Indicate that the event was not handled
