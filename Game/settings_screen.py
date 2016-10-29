from kivy.uix.screenmanager import ScreenManager, Screen
from base_screen import BaseScreen
from kivy.uix.button import Button


def restore_state(func):
    def decorated(*args, **kwargs):
        args[1].background_color = (1, 1, 1, 1)
        return func(*args, **kwargs)
    return decorated


class SettingIcon(Button):
    """Icon class."""

    def __init__(self, **kwargs):
        """Init icon."""
        self.name = None# kwargs['name']
        super(SettingIcon, self).__init__()

    def late_init(self, **kwargs):
        """Populate icon."""
        self.name = kwargs['name']
        #self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        """Set background image."""
        pass

    def on_press(self):
        self.background_color = (0.5, 0.5, 0.5, 1)

class SettingsScreen(BaseScreen):

    POSITIONS_X = {0: 728 / 2048.0}
    POSITIONS_Y = {0: (1536. - 1400) / 1536.0}
    SIZES = {0: (730 / 2048.0, (1536 - 1340) / 1536.0)}

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(SettingsScreen, self).__init__(**kwargs)
        self.sm = sm
        self.name = kwargs['name']
        self.menu_screen = kwargs['menu']

        self.back_button = self.ids['Back']

        self.back_button.late_init(**{'name': 'Back', 'image': 'assets/settings/btn_back_active.png'})
        self.back_button.bind(on_release=self.pressed_back)
        self.back_button.pos_hint = {'x': self.POSITIONS_X[0],
                                     'y': self.POSITIONS_Y[0]}
        self.back_button.size_hint = self.SIZES[0]
        self.back_button.render()
        self.back_button.show()

    @restore_state
    def pressed_back(self, *args):
        #self.sm.add_widget(self.menu_screen)
        self.sm.current = 'startscreen'
        #print "pressed back"
        #self.sm.switch_to(self.menu_screen)
