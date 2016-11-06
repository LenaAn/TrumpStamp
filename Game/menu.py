from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.graphics.vertex_instructions import Ellipse

import start_screen


class MenuButton(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.window = Button()
        self.show_end_game_button = Button()
        self.show_restart_button = Button()
        self.end_game_button = Button()
        self.restart_game_button = Button()
        self.continue_button = Button()
        self.new_game_window = Button()

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
            Ellipse(source='assets/buttons/menu_btn_p.png', pos=self.pos, size=self.size)
        print "continue game"

    def continue_game_from_restart(self, button):
        self.parent.remove_widget(self.continue_button)
        self.parent.remove_widget(self.new_game_window)
        self.parent.remove_widget(self.restart_game_button)

        for child in self.parent.children:
            child.disabled = False
        with self.canvas:
            Ellipse(source='assets/buttons/menu_btn_p.png', pos=self.pos, size=self.size)
        print "continue game"

    def continue_game_from_end_game(self, button):
        self.parent.remove_widget(self.continue_button)
        self.parent.remove_widget(self.new_game_window)
        self.parent.remove_widget(self.end_game_button)

        for child in self.parent.children:
            child.disabled = False
        with self.canvas:
            Ellipse(source='assets/buttons/menu_btn_p.png', pos=self.pos, size=self.size)
        print "continue game"

    def start_new_game(self, *args):
        start_screen_ = start_screen.StartScreen(self.parent.sm, name="startscreen")
        self.parent.sm.switch_to(start_screen_)

    def show_restart(self, button):
        self.parent.remove_widget(self.show_end_game_button)
        self.parent.remove_widget(self.show_restart_button)
        self.parent.remove_widget(self.continue_button)
        self.parent.remove_widget(self.window)

        self.parent.add_widget(self.new_game_window)
        self.new_game_window.background_normal = 'assets/menu/menu_10.png'
        self.new_game_window.background_down = 'assets/menu/menu_10.png'
        self.new_game_window.size_hint = (0.5, 0.5)
        self.new_game_window.pos_hint = {'x': 0.25, 'y': 0.25}
        self.new_game_window.border = (0, 0, 0, 0)

        self.parent.add_widget(self.continue_button)
        self.continue_button.opacity = 0
        self.continue_button.size_hint = (0.35, 0.07)
        self.continue_button.pos_hint = {'x': 0.35, 'y': 0.3}
        self.continue_button.bind(on_press=self.continue_game_from_restart)

        self.parent.add_widget(self.restart_game_button)
        self.restart_game_button.opacity = 0
        self.restart_game_button.size_hint = (0.35, 0.07)
        self.restart_game_button.pos_hint = {'x': 0.35, 'y': 0.39}
        self.restart_game_button.bind(on_press=self.start_new_game)

    def show_end_game(self, button):
        self.parent.remove_widget(self.show_end_game_button)
        self.parent.remove_widget(self.show_restart_button)
        self.parent.remove_widget(self.continue_button)
        self.parent.remove_widget(self.window)

        self.parent.add_widget(self.new_game_window)
        self.new_game_window.background_normal = 'assets/menu/menu_11.png'
        self.new_game_window.background_down = 'assets/menu/menu_11.png'
        self.new_game_window.size_hint = (0.5, 0.5)
        self.new_game_window.pos_hint = {'x': 0.25, 'y': 0.25}
        self.new_game_window.border = (0, 0, 0, 0)

        self.parent.add_widget(self.continue_button)
        self.continue_button.opacity = 0
        self.continue_button.size_hint = (0.35, 0.07)
        self.continue_button.pos_hint = {'x': 0.35, 'y': 0.3}
        self.continue_button.bind(on_press=self.continue_game_from_end_game)

        self.parent.add_widget(self.end_game_button)
        self.end_game_button.opacity = 0
        self.end_game_button.size_hint = (0.35, 0.07)
        self.end_game_button.pos_hint = {'x': 0.35, 'y': 0.39}
        self.end_game_button.bind(on_press=self.start_new_game)

    def on_press(self):
        with self.canvas:
            Ellipse(source='assets/buttons/menu_btn_a.png', pos=self.pos, size=self.size)

        for child in self.parent.children:
            child.disabled = True

        self.parent.add_widget(self.window)
        self.window.background_normal = 'assets/menu/menu_00.png'
        self.window.background_down = 'assets/menu/menu_00.png'
        self.window.size_hint = (0.5, 0.5)
        self.window.pos_hint = {'x': 0.25, 'y': 0.25}
        self.window.border = (0, 0, 0, 0)

        self.parent.add_widget(self.show_restart_button)
        self.show_restart_button.opacity = 0
        self.show_restart_button.size_hint = (0.35, 0.07)
        self.show_restart_button.pos_hint = {'x': 0.35, 'y': 0.48}
        self.show_restart_button.bind(on_press=self.show_restart)

        self.parent.add_widget(self.show_end_game_button)
        self.show_end_game_button.opacity = 0
        self.show_end_game_button.size_hint = (0.35, 0.07)
        self.show_end_game_button.pos_hint = {'x': 0.35, 'y': 0.39}
        self.show_end_game_button.bind(on_press=self.show_end_game)

        self.parent.add_widget(self.continue_button)
        self.continue_button.opacity = 0
        self.continue_button.size_hint = (0.35, 0.07)
        self.continue_button.pos_hint = {'x': 0.35, 'y': 0.3}
        self.continue_button.bind(on_press=self.continue_game)
