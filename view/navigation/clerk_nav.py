from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.clock import Clock
# from controller.user_controller import UserController
from kivy.lang import Builder
# from kivy.core.window import Window
# from kivy.uix.boxlayout import BoxLayout

# Builder.load_file('view/UI.kv')
Builder.load_file('view/navigation/clerk_nav.kv')


class ClerkNav(Screen):
    def __init__(self, **kwargs):
        super(ClerkNav, self).__init__(**kwargs)
        # self.controller = UserController()

# class CommonNavigationRailItem(MDNavigationRailItem):
#     text = StringProperty()
#     icon = StringProperty()
    
# class ExtendedButton(MDFillRoundFlatIconButton, CommonElevationBehavior):
#     '''
#     Implements a button of type
#     `Extended FAB <https://m3.material.io/components/extended-fab/overview>`_.

#     .. rubric::
#         Extended FABs help people take primary actions.
#         They're wider than FABs to accommodate a text label and larger target
#         area.

#     This type of buttons is not yet implemented in the standard widget set
#     of the KivyMD library, so we will implement it ourselves in this class.
#     '''

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.padding = "16dp"
#         Clock.schedule_once(self.set_spacing)

#     def set_spacing(self, interval):
#         self.ids.box.spacing = "12dp"

#     def set_radius(self, *args):
#         if self.rounded_button:
#             self._radius = self.radius = self.height / 4