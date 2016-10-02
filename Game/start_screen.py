"""Start screen module."""
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
import elections_game


class Icon(Button):
    """Icon class."""

    def __init__(self, **kwargs):
        """Init icon."""
        self.game = None
        self.name = None
        self.image = None
        super(Icon, self).__init__()

    def late_init(self, **kwargs):
        """Populate icon."""
        self.name = kwargs['name']
        self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        """Set background image."""
        self.background_normal = self.image
        self.background_down = self.image


class StartScreen(Screen):
    """Start screen class."""

    POSITIONS_X = {0: 190 / 2048.0,
                   1: 1158 / 2048.0}
    POSITIONS_Y = {0: (1536.0 - 1400.0) / 1536.0,
                   1: (1536.0 - 1400.0) / 1536.0}

    SIZES = {0: (700 / 2048.0, (1536 - 600) / 1536.0)}

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(StartScreen, self).__init__(**kwargs)
        trump_data = {'name': 'Trump', 'image': 'assets/Trump.png'}
        hillary_data = {'name': 'Hillary', 'image': 'assets/Hillary.png'}
        datas = [trump_data, hillary_data]
        self.icon_trump = self.ids['IconTrump']
        self.icon_hillary = self.ids['IconHillary']
        self.icons = [self.icon_trump, self.icon_hillary]

        self.game = elections_game.ElectionsGame(sm, name="electionsgame")
        self.sm = sm
        #sm.add_widget(self)

        for i in [0, 1]:
            self.icons[i].late_init(**datas[i])
            self.icons[i].show()
            self.icons[i].pos_hint = {'x': self.POSITIONS_X[i],
                                      'y': self.POSITIONS_Y[i]}
            self.icons[i].size_hint = self.SIZES[0]
            self.icons[i].render()

        self.icons[0].bind(on_press=self.pressed_trump)
        self.icons[1].bind(on_press=self.pressed_hillary)

    def pressed_trump(self, *args):
        """Trump choice callback."""
        self.game.set_bot('hillary')
        self.sm.switch_to(self.game)

    def pressed_hillary(self, *args):
        """Hillary choice callback."""
        self.game.set_bot('trump')
        self.sm.switch_to(self.game)
