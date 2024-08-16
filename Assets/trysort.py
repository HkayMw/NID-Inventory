from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

class CustomCanvas(Widget):
    pass

class MyApp(App):
    def build(self):
        return BoxLayout()

if __name__ == '__main__':
    MyApp().run()
