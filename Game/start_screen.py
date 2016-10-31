"""Start screen module."""
from kivy.uix.button import Button
import elections_game
from base_screen import BaseScreen
from settings_screen import SettingsScreen
from credits_screen import CreditScreen
from rounds_screen import RoundsScreen
import tracker
from sound_manager import SoundManager


def restore_state(func):
    def decorated(*args, **kwargs):
        args[1].background_color = (1, 1, 1, 1)
        return func(*args, **kwargs)
    return decorated

class Icon(Button):
    """Icon class."""

    def __init__(self, **kwargs):
        """Init icon."""
        #self.game = None
        self.name = None
        self.image = None
        super(Icon, self).__init__()

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


class StartScreen(BaseScreen):
    """Start screen class."""

    sound_start = 'assets/sounds/cnn_election.wav'

    POSITIONS_X = {0: 1128 / 2048.0,
                   1: 190 / 2048.0,
                   2: 680 / 2048.,
                   3: 680 / 2048.}
    POSITIONS_Y = {0: (1536.0 - 730.0) / 1536.0,
                   1: (1536.0 - 730.0) / 1536.0,
                   2: (1536 - 1130) / 1536.,
                   3: (1536 - 1400) / 1536.}

    SIZES = {0: (730 / 2048.0, (1536 - 1340) / 1536.0)}

    def __init__(self, sm, **kwargs):
        """Init start screen."""
        super(StartScreen, self).__init__(**kwargs)

        SoundManager.play_audio(self.sound_start, loop=True)

        trump_data = {'name': 'Trump'}
        hillary_data = {'name': 'Hillary'}
        settings_data = {'name': 'Settings'}
        credits_data = {'name': 'Credit'}


        datas = [trump_data, hillary_data, settings_data, credits_data]
        self.icon_trump = self.ids['Trump']
        self.icon_hillary = self.ids['Hillary']
        self.icon_settings = self.ids['Settings']
        self.icon_credit = self.ids['Credit']
        self.icons = [self.icon_trump, self.icon_hillary, self.icon_settings, self.icon_credit]

        #self.game = elections_game.ElectionsGame(sm, name="electionsgame")
        self.rounds = RoundsScreen(sm, name='rounds', menu=self)
        self.settings = SettingsScreen(sm, name='settings', menu=self)
        self.credit = CreditScreen(sm, name='credit', menu=self)
        self.sm = sm

        for i in range(0,4):
            self.icons[i].late_init(**datas[i])
            self.icons[i].show()
            self.icons[i].pos_hint = {'x': self.POSITIONS_X[i],
                                      'y': self.POSITIONS_Y[i]}

            self.icons[i].size_hint = self.SIZES[0]
            self.icons[i].render()

        self.icons[0].bind(on_release=self.pressed_trump)
        self.icons[1].bind(on_release=self.pressed_hillary)
        self.icons[2].bind(on_release=self.pressed_setting)
        self.icons[3].bind(on_release=self.pressed_credit)

    @restore_state
    def pressed_trump(self, *args):
        """Trump choice callback."""
        SoundManager.stop_audio(self.sound_start)
        # self.game.set_bot('hillary')
        # self.sm.switch_to(self.game)
        tracker.tracker.send(tracker.EventBuilder().set(ec="user action",
                                                        ea="selected trump").build())
        self.rounds.set_bot('hillary')
        self.pressed_round()

    @restore_state
    def pressed_hillary(self, *args):
        """Hillary choice callback."""
        SoundManager.stop_audio(self.sound_start)
        #self.game.set_bot('trump')
        #self.sm.switch_to(self.game)
        tracker.tracker.send(tracker.EventBuilder().set(ec="user action",
                                                        ea="selected hillary").build())
        self.rounds.set_bot('trump')
        self.pressed_round()

    @restore_state
    def pressed_setting(self, *args):

        if not self.sm.has_screen('settings'):
            self.sm.add_widget(self.settings)

        self.sm.current = 'settings'

    @restore_state
    def pressed_credit(self, *args):

        if not self.sm.has_screen('credit'):
            self.sm.add_widget(self.credit)

        self.sm.current = 'credit'

    def pressed_round(self):

        if not self.sm.has_screen('rounds'):
            self.sm.add_widget(self.rounds)

        self.sm.current = 'rounds'
