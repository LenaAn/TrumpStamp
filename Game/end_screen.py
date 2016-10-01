"""End screen module."""
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button


class EndScreen(Screen):
    """End screen class."""

    def __init__(self, winner_name, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        self.winner_name = winner_name
