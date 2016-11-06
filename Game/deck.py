"""Deck module."""
import kivy
import random
kivy.require('1.7.2')


class Deck():
    """Deck class."""

    def __init__(self, player, card_factory):
        """Init deck."""
        self.player = player
        self.num_deals = 0
        self.cards = [card_factory.get_card(i, player.get_player_id(), player.bot) for i in xrange(1, 54)]
        self.returned_cards = []

    def get_owner(self):
        """Return deck owner."""
        return self.player

    def shuffle(self):
        """Shuffle cards."""
        random.shuffle(self.cards)

    def pop_card(self):
        """Remove card from deck."""
        if self.num_deals % 30 == 0:
            self.cards.extend(self.returned_cards)
            self.returned_cards = []
            self.shuffle()
        self.num_deals += 1
        return self.cards.pop()

    def return_card_to_deck(self, card):
        self.returned_cards.append(card)
