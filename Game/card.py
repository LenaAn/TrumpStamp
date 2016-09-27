from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
import csv
import os

ZOOM_SCALE_FACTOR = 1.5
DELAY_TIME = 0.5

class Card(Button):
    # Workaround, need to use Deck instead
    current_zoomed_in_card = None

    def __init__(self, **kwargs):
        self.card_id = kwargs.pop('id')
        self.description = kwargs['description']
        self.name = kwargs['title']
        self.cost_color = kwargs['cost_color']
        self.cost_value = kwargs['cost_value']
        super(Card, self).__init__(**kwargs)
        self.game = kwargs['game']
        self.owner_id = kwargs['owner_id']
        self.actions = kwargs['actions']
        self.image = kwargs['image_path']
        self.background = kwargs['background']
        self.counter_for_expand = 0
        self.touch_moving = False

        self.background_normal = self.background
        self.background_down = self.background
        self.sound = SoundLoader.load(kwargs['sound'])
        self.touch_moving = False
        self.size = [self.size_hint[0], self.size_hint[1]]
        self.zoomed_in = False
        self.is_bot = self.game.PLAYERS[self.owner_id].is_bot()
        super(Card, self).__init__()

    def __repr__(self):
        return '{0} = {4}{1} ({2}/{3})'.format(self.card_id, self.name,
                                               self.cost_color, self.cost_value,
                                               self.description)

    def __eq__(self, other):
        return (isinstance(other, Card) and other.card_id == self.card_id and
                other.owner_id == self.owner_id)

    def render(self):
        if not self.parent:
            self.game.add_widget(self)

    def delete(self, *args, **kwargs):
        if self.parent:
            self.game.remove_widget(self)

    def bring_to_front(self):
        self.delete()
        self.render()

    def show(self):
        self.background_normal = self.image
        self.background_down = self.image

    def hide(self):
        self.background_normal = self.background
        self.background_down = self.background

    def use(self):
        if self.game.card_clicked(self):
            self.bring_to_front()
            if self.is_bot:
                anim = (Animation(d=DELAY_TIME) + self._build_use_anim())
            else:
                anim = self._build_use_anim()
            if Card.current_zoomed_in_card is not None:
                Card.current_zoomed_in_card.zoom_out()
            anim.start(self)
            self.play_sound()
        else:
            self.on_deny()

    def drop(self):
        if self.game.card_dropped(self):
            if Card.current_zoomed_in_card is not None:
                Card.current_zoomed_in_card.zoom_out()
            if self.is_bot:
                anim = Animation(d=DELAY_TIME) + self._build_drop_anim()
            else:
                anim = self._build_drop_anim()
            anim.bind(on_complete=self.delete)
            anim.start(self)
            self.play_sound()
        else:
            self.on_deny()

    def zoom_in(self):
        if not self.zoomed_in:
            self.bring_to_front()
            self._build_zoom_in_anim().start(self)
            Card.current_zoomed_in_card = self
            self.zoomed_in = True
            return True
        else:
            return False

    def zoom_out(self):
        if self.zoomed_in:
            self._build_zoom_out_anim().start(self)
            Card.current_zoomed_in_card = None
            self.zoomed_in = False
            return True
        else:
            return False

    def _build_zoom_in_anim(self):
        card = self
        delta_x = self.size_hint[0] * ZOOM_SCALE_FACTOR / 5
        return (Animation(size_hint=(card.size_hint[0] * ZOOM_SCALE_FACTOR,
                                     card.size_hint[1] * ZOOM_SCALE_FACTOR),
                          duration=0.25) &
                Animation(pos_hint={'x': card.pos_hint['x'] - delta_x,
                          'y': card.pos_hint['y']}, duration=0.25))

    def _build_zoom_out_anim(self):
        card = self
        delta_x = self.size_hint[0] / 5
        return (Animation(size_hint=(card.size_hint[0] / ZOOM_SCALE_FACTOR,
                                     card.size_hint[1] / ZOOM_SCALE_FACTOR),
                          duration=0.25) &
                Animation(pos_hint={'x': card.pos_hint['x'] + delta_x,
                                    'y': card.pos_hint['y']}, duration=0.25))

    def _build_use_anim(self):
        if self.owner_id:
            x_pos = 720.0
        else:
            x_pos = 1070.0
        y_pos = 536.0
        return Animation(pos_hint={'x': x_pos / 2048.0,
                                   'y':  y_pos / 1536.0},
                         duration=0.5)

    def _build_drop_anim(self):
        x, y = self.pos_hint["x"], self.pos_hint["y"]
        if self.owner_id:
            return (Animation(pos_hint={"x": x, "y": y + 0.1}, duration=0.2) +
                Animation(opacity=0, duration=0.2))
        else:
            return (Animation(pos_hint={"x": x, "y": y - 0.1}, duration=0.2) +
                Animation(opacity=0, duration=0.2))

    def _build_deny_anim(self):
        anim = Animation(pos_hint={'x': self.pos_hint['x'] + 15 / 2048.0, 'y': self.pos_hint['y']},
                         duration=0.025)
        anim += Animation(pos_hint={'x': self.pos_hint['x'] - 15 / 2048.0, 'y': self.pos_hint['y']},
                          duration=0.05)
        anim += Animation(pos_hint={'x': self.pos_hint['x'] + 15 / 2048.0, 'y': self.pos_hint['y']},
                          duration=0.05)
        anim += Animation(pos_hint={'x': self.pos_hint['x'], 'y': self.pos_hint['y']},
                          duration=0.025)
        return anim

    def get_owner(self):
        return self.owner_id

    def get_cost(self):
        return self.cost_color, self.cost_value

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.orig_pos = touch.pos
            self.touch_moving = True
            return True

    def on_touch_up(self, touch):
        if self.touch_moving:
            if ((touch.pos[0] - self.orig_pos[0]) ** 2 +
                    (touch.pos[1] - self.orig_pos[1]) ** 2) < 25:
                pass
                if self.zoomed_in:
                    self.zoom_out()
                else:
                    if Card.current_zoomed_in_card:
                        Card.current_zoomed_in_card.zoom_out()
                    self.zoom_in()
            if touch.pos[1] - self.orig_pos[1] > 20:
                if self.owner_id:
                    self.drop()
                else:    
                    self.use()
            if self.orig_pos[1] - touch.pos[1] > 20:
                if self.owner_id:
                    self.use()
                else:
                    self.drop()
            self.touch_moving = False
            return True

    def on_deny(self):
        self._build_deny_anim().start(self)

    def get_actions(self):
        # {'player': [(type, value)], 'opponent': [(type, value)]}
        actions = {'player': [],
                   'opponent': []}
        for action in self.actions:
            action_value = action[0]
            action_type = action[1]
            action_affects = action[2]
            action_ = (action_type, action_value)
            if action_affects == 0:
                actions['player'].append(action_)
            elif action_affects == 1:
                actions['opponent'].append(action_)
            else:
                actions['player'].append(action_)
                actions['opponent'].append(action_)
        return actions

    def play_sound(self):
        self.sound.play()


class CardFabric(object):
    def __init__(self, game, card_db, images_path=None, sound_path=None, background_path=None):
        self.db = []
        with open(card_db) as card_file:
            reader = csv.DictReader(card_file)
            str_keys = ['t_title', 'h_title', 'description', 'img_t', 'img_h']
            for row in reader:
                row_ = {k: (int(v) if k not in str_keys else v) for k, v in row.iteritems()}
                self.db.append(row_)
        self.images_path = images_path or {'trump': 'assets/cards/trump',
                                           'hillary': 'assets/cards/hillary'}
        self.sound_path = sound_path or 'assets/stubs/Sounds/card.wav'
        self.background_path = background_path or 'assets/card00.png'
        self.game = game

    def get_card(self, card_id, owner_id):
        card_data = dict(self.db[card_id - 1])
        card_data['owner_id'] = owner_id
        card_data['description'] = card_data['description'].replace('*', '; ')
        if owner_id == 0:
            card_data['title'] = card_data['t_title'].replace('*', ' ')
            card_data['image_path'] = (os.path.join(self.images_path['trump'], card_data['img_t']) +
                                       '.png')
        elif owner_id == 1:
            card_data['title'] = card_data['h_title'].replace('*', ' ')
            card_data['image_path'] = (os.path.join(self.images_path['hillary'],
                                       card_data['img_h']) + '.png')
        else:
            raise ValueError('Wrong owner_id')
        actions = [[card_data['act1_value'], card_data['act1_type'], card_data['act1_side']],
                   [card_data['act2_value'], card_data['act2_type'], card_data['act2_side']],
                   [card_data['act3_value'], card_data['act3_type'], card_data['act3_side']]]
        card_data['actions'] = actions
        card_data['sound'] = self.sound_path
        card_data['background'] = self.background_path

        card = Card(game=self.game, **card_data)
        return card


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    cards = CardFabric(None, os.path.join(SCRIPT_DIR, 'cards.csv'))
