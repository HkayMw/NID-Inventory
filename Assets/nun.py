from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Add a common header
        self.header = Label(text="Header", size_hint_y=None, height=50)
        self.add_widget(self.header)

        # Create ScreenManager for switching between subscreens
        self.screen_manager = ScreenManager()
        self.add_widget(self.screen_manager)

        # Add screens to the ScreenManager
        self.screen_manager.add_widget(ScreenOne(name='screen_one'))
        self.screen_manager.add_widget(ScreenTwo(name='screen_two'))

        # Add a common footer with navigation buttons
        footer = BoxLayout(size_hint_y=None, height=50)
        btn_screen_one = Button(text="Go to Screen One", on_release=self.go_to_screen_one)
        btn_screen_two = Button(text="Go to Screen Two", on_release=self.go_to_screen_two)
        footer.add_widget(btn_screen_one)
        footer.add_widget(btn_screen_two)
        self.add_widget(footer)

    def go_to_screen_one(self, instance):
        self.screen_manager.current = 'screen_one'

    def go_to_screen_two(self, instance):
        self.screen_manager.current = 'screen_two'

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        self.add_widget(Label(text="This is Screen One"))

class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        self.add_widget(Label(text="This is Screen Two"))

class MyApp(App):
    def build(self):
        return MainScreen()
    
    

if __name__ == '__main__':
    MyApp().run()
