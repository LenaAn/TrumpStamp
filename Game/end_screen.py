from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from base_screen import BaseScreen
import start_screen, rounds_screen, elections_game
from kivy.core.audio import SoundLoader

def restore_state(func):
    def decorated(*args, **kwargs):
        args[1].background_color = (1, 1, 1, 1)
        return func(*args, **kwargs)
    return decorated


class EndGameIcon(Button):
    def __init__(self, **kwargs):
        self.image = None
        super(EndGameIcon, self).__init__()

    def late_init(self, **kwargs):
        self.image = kwargs['image']

    def render(self):
        if not self.parent:
            print("Render {}".format(self.name))

    def show(self):
        self.background_normal = self.image
        self.background_down = self.image

    def on_press(self):
        self.background_color = (0.5, 0.5, 0.5, 1)


class EndScreen(BaseScreen):

    sound_tramp_path = 'assets/sounds/tramp_sound.mp3'
    sound_hillary_path = 'assets/sounds/hillary_sound.mp3'

    POSITIONS_X = {0: 653 / 2048.0,
                   1: 668 / 2048.0}
    POSITIONS_Y = {0: 643 / 1536.0,
                   1: 980 / 1536.0}

    SIZES = {0: (740 / 2048.0, 240 / 1536.0),
             1: (715 / 2048.0, 157 / 1536.0),
             2: (1, 1)}

    def __init__(self, sm, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        self.winner_name = kwargs['winner']
        self.bot_name = kwargs['bot']
        self.round_id = kwargs['round']
        self.store = kwargs['store']
        self.state = kwargs['state']
        self.area = kwargs['area']
        self.menu_screen = kwargs['menu_screen']
        new_game_image = {'image': 'assets/out.png'}
        winner_image = dict()

        if self.winner_name == 'Trump':
            self.sound = SoundLoader.load(self.sound_tramp_path)
            self.sound.play()
            self.sound.loop = True
            winner_image['image'] = 'assets/win_trump.png'
        elif self.winner_name == 'Hillary':
            self.sound = SoundLoader.load(self.sound_hillary_path)
            self.sound.play()
            self.sound.loop = True
            winner_image['image'] = 'assets/win_hillary.png'

        self.new_game_icon = self.ids['NewGame']
        self.winner_icon = self.ids['Winner']
        self.next_game_icon = self.ids['NextGame']
        self.restart_game_icon = self.ids['RestartGame']

        self.sm = sm

        self.new_game_icon.late_init(**new_game_image)
        self.new_game_icon.show()
        self.new_game_icon.pos_hint = {'x': self.POSITIONS_X[0],
                                       'y': self.POSITIONS_Y[0]}
        self.new_game_icon.size_hint = self.SIZES[0]
        self.new_game_icon.render()

        self.new_game_icon.bind(on_release=self.pressed_new_game)

        self.winner_icon.late_init(**winner_image)
        self.winner_icon.show()
        self.winner_icon.pos_hint = {'x': 0,
                                     'y': 0}
        self.winner_icon.size_hint = self.SIZES[2]
        self.winner_icon.render()

        self.next_game_icon.pos_hint = {'x': 0.28,
                                        'y': 0.18}
        self.next_game_icon.size_hint = (0.45, 0.08)
        self.next_game_icon.background_color = (0, 0, 0, 0)
        self.next_game_icon.bind(on_release=self.pressed_new_game)

        self.restart_game_icon.pos_hint = {'x': 0.28,
                                           'y': 0.28}
        self.restart_game_icon.size_hint = (0.45, 0.08)
        self.restart_game_icon.background_color = (0, 0, 0, 0)
        self.restart_game_icon.bind(on_release=self.pressed_restart_game)

    @restore_state
    def pressed_restart_game(self, *args):
        self.sound.stop()
        self.game = elections_game.ElectionsGame(self.sm, name="electionsgame")
        self.game.set_bot(self.bot_name)
        print('pressed_restart_game')
        self.game.set_store(self.store)
        self.game.set_round(self.round_id, self.state, self.area)
        self.sm.switch_to(self.game)

    @restore_state
    def pressed_new_game(self, *args):
        self.sound.stop()
        if not self.bot_name == self.winner_name.lower():
            self.store.put(str(self.round_id), won=True)
        print('pressed_new_game')
        self.menu_screen = start_screen.StartScreen(self.sm, name="startscreen")
        self.menu_screen.rounds = rounds_screen.RoundsScreen(self.sm, name='rounds', menu=self.menu_screen)
        self.menu_screen.rounds.set_bot(self.bot_name)
        self.sm.switch_to(self.menu_screen.rounds)
