from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.graphics.vertex_instructions import Ellipse

import start_screen


class HelpButton(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        super(HelpButton, self).__init__(**kwargs)
        self.window = Button()
        with open('assets/help/help.txt', 'r') as f:
            self.window.text = f.read()
        # self.window.halign = 'center'
        self.window.line_height = 1.5
        self.bind(on_press=self.on_press_show)

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def continue_game(self, button):
        self.parent.remove_widget(self.show_end_game_button)
        self.parent.remove_widget(self.show_restart_button)
        self.parent.remove_widget(self.continue_button)
        self.parent.remove_widget(self.window)

        for child in self.parent.children:
            child.disabled = False
        with self.canvas:
            Ellipse(source='assets/buttons/help_btn_p.png', pos=self.pos, size=self.size)
        print "continue game"

    def on_press_show(self, touch):
        print "On press show help"
        with self.canvas:
            Ellipse(source='assets/buttons/help_btn_a.png', pos=self.pos, size=self.size)

        for child in self.parent.children:
            child.disabled = True

        self.disabled = False

        self.parent.add_widget(self.window)
        self.window.background_normal = 'assets/help/help.png'
        self.window.background_down = 'assets/help/help.png'
        self.window.size_hint = (1.0, 0.92)
        self.window.opacity = 0.8
        self.window.pos_hint = {'x': 0.0, 'y': 0.0}
        self.window.border = (0, 0, 0, 0)

        self.unbind(on_press=self.on_press_show)
        self.bind(on_press=self.on_press_hide)

    def on_press_hide(self, touch):
        print "On press hide help"
        with self.canvas:
            Ellipse(source='assets/buttons/help_btn_p.png', pos=self.pos, size=self.size)

        for child in self.parent.children:
            child.disabled = False

        self.parent.remove_widget(self.window)

        self.unbind(on_press=self.on_press_hide)
        self.bind(on_press=self.on_press_show)
