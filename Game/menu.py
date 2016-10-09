from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector


# class MenuIcon(Button):
#     def __init__(self, **kwargs):
#         self.image = None
#         super(MenuIcon, self).__init__()
#
#     def late_init(self, **kwargs):
#         self.image = kwargs['image']
#
#     def render(self):
#         if not self.parent:
#             print("Render {}".format(self.name))
#
#     def show(self):
#         self.background_normal = self.image
#         self.background_down = self.image



class MenuButton(Button, ButtonBehavior):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.background_normal = 'assets/buttons/btn_menu_inactive.png'
        self.background_down = 'assets/buttons/btn_menu_active.png'

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def on_press(self):
        self.background_normal = 'assets/buttons/btn_menu_inactive.png'
        self.background_down = "assets/buttons/btn_menu_inactive.png"
        self.canvas. = 'assets/buttons/btn_menu_inactive.png'
        self.show()
        print("Lena")

    def show(self):
        self.background_normal = 'assets/buttons/btn_menu_inactive.png'
        self.background_down = "assets/buttons/btn_menu_inactive.png"

