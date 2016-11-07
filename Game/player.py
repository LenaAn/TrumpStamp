"""Player module."""
from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty
from kivy.uix.widget import Widget
from deck import Deck
from hand import Hand

PLAYERS = {0: 'trump_player',
           1: 'hillary_player'}


class Player(Widget):
    """Player class."""

    partisans = BoundedNumericProperty(0, min=0, rebind=True)
    swing = BoundedNumericProperty(0, min=0)
    media = BoundedNumericProperty(1, min=1)
    news = BoundedNumericProperty(1, min=0)
    mojo = BoundedNumericProperty(1, min=1)
    hype = BoundedNumericProperty(1, min=0)
    money = BoundedNumericProperty(1, min=1)
    cash = BoundedNumericProperty(1, min=0)
    state_area = ObjectProperty('')

    cards_actions = ListProperty([])

    def __init__(self, **kwargs):
        """Init player."""
        super(Player, self).__init__(**kwargs)
        self.player_id = None
        self.player_name = None
        self.stats = None

    def __str__(self):
        return str(type(self))

    def late_init(self, **kwargs):
        """Init player resources."""
        self.player_id = kwargs.pop('player_id')
        self.card_factory = kwargs.pop('card_factory')
        is_bot = kwargs.pop('is_bot')
        self.human = False if is_bot else True
        self.bot = True if is_bot else False
        self.player_name = PLAYERS[self.player_id]
        self.stats = kwargs
        for prop_name, value in self.stats.items():
            self.property(prop_name).set(self, value)

        self.RESOURSES = {1: 'news', 2: 'cash', 3: 'hype'}
        self.ACTIONS = {1: ['swing'], 2: ['partisans'], 3: ['news'], 4: ['hype'], 5: ['cash'],
                        6: ['media'], 7: ['mojo'], 8: ['money'], 9:  ['news', 'hype', 'cash'],
                        10: ['media', 'mojo', 'money']}
        self.active = False
        self.winner = None

        self.deck = Deck(self, self.card_factory)
        self.hand = Hand(self.deck)

    def set_opponent(self, opponent):
        """Set player's opponent."""
        self.opponent = opponent

    def set_active(self, active):
        """Set player as active."""
        self.active = active

    def get_active(self):
        """See if player is active."""
        return self.active

    def is_bot(self):
        """See if player is bot."""
        return self.bot

    def set_winner(self, winner):
        """Make player winner or loser."""
        self.winner = winner

    def get_deck(self):
        """Get deck."""
        return self.deck

    def get_hand(self):
        """Get player hand."""
        return self.hand

    def get_player_id(self):
        """Get player id."""
        return self.player_id

    def get_voters(self):
        """Get number of partisans."""
        return self.partisans

    def play(self):
        pass

    def pay_for_card(self, card_color, card_value):
        """If possible pay for card."""
        if card_color != 0 and card_color != 4:
            property = self.property(self.RESOURSES[card_color])
            property_value = property.get(self)
            if (property_value - card_value) >= 0:
                property.set(self, property_value - card_value)
            else:
                return False
        else:
            for color, prop_name in self.RESOURSES.items():
                property = self.property(prop_name)
                property_value = property.get(self)
                if (property_value - card_value) >= 0:
                    property.set(self, property_value - card_value)
                else:
                    return False
        return True

    def apply_card(self, type, value):
        """
        Apply card actions.

        Return True if after applying this card the turn doesn't change.
        """
        if type == 0:
            if value >= 0:
                self.swing += value
            # lose voters branch
            elif value < 0:
                diff = self.swing + value
                self.swing = max(0, self.swing + value)
                if diff < 0:
                    self.partisans = max(0, self.partisans + diff)
        elif type == 11:
            return True
        else:
            for res in self.ACTIONS[type]:
                # TODO:
                # check with -value, it seems that it doesn't work((
                old_value = self.property(res).get(self)
                min_value = self.property(res).get_min(self)
                # print self.player_id, res, type, value, old_value, min_value
                self.property(res).set(self, max(min_value, old_value + value))
        return False

    def update_resources(self):
        """Update resources of players at the end of the turn."""
        for increment, resource in (('media', 'news'), ('mojo', 'hype'), ('money', 'cash')):
            increment_property = self.property(increment)
            increment_property_value = increment_property.get(self)
            resource_property = self.property(resource)
            resource_property_value = resource_property.get(self)
            resource_property.set(self, increment_property_value + resource_property_value)

    def check_resources(self):
        for i, resource in (('media', 'news'), ('mojo', 'hype'), ('money', 'cash')):
            resource_property = self.property(resource)
            resource_property_value = resource_property.get(self)
            if resource_property_value >= 300:
                return True
        return False

            
