import kivy
import os
import csv
from collections import defaultdict
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from card import CardFactory
from kivy.animation import Animation
from player import Player
from end_screen import EndScreen
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from bots import *

kivy.require('1.7.2')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

round_csv = os.path.join(SCRIPT_DIR, 'rounds.csv')
cards_csv = os.path.join(SCRIPT_DIR, 'cards.csv')


class ElectionsGame(Screen):
    """
       This class represents the game.
       As a Kivy object it represents the game field and is a root for all other
       objects. As a general class it stores all the stuff in the game.
    """
    def __init__(self, sm, **kwargs):
        super(ElectionsGame, self).__init__(**kwargs)
        self.card_factory = CardFactory(self, cards_csv)
        self.sm = sm

    def set_bot(self, bot_name):
        round_id = 0
        if bot_name == 'trump':
            self.trump = RandomPressBot(self.ids['trump_player'])
            self.hillary = self.ids['hillary_player']
        elif bot_name == 'hillary':
            self.hillary = RandomPressBot(self.ids['hillary_player'])
            self.trump = self.ids['trump_player']

        self.PLAYERS = {0: self.trump,
                        1: self.hillary}
        # self.card_factory = CardFactory(self, cards_csv)

        round_db = []
        with open(round_csv) as round_file:
            reader = csv.DictReader(round_file)
            for row in reader:
                row_ = {k: int(v) for k, v in row.iteritems()}
                round_db.append(row_)

        self.victory = {'destr': round_db[round_id]['destr'], 'res': round_db[round_id]['res']}
        # CREATE PLAYERS
        # parameters are labeled as t0-t1, digit points to resource code per card database
        print(round_db)
        self.trump.late_init(
            player_id=0,
            swing=round_db[round_id]['t1'],
            partisans=round_db[round_id]['t2'],
            news=round_db[round_id]['t3'],
            hype=round_db[round_id]['t4'],
            cash=round_db[round_id]['t5'],
            media=round_db[round_id]['t6'],
            mojo=round_db[round_id]['t7'],
            money=round_db[round_id]['t8'],
            card_factory=self.card_factory,
            is_bot=False if bot_name == 'hillary' else True)
        self.hillary.late_init(
            player_id=1,
            swing=round_db[round_id]['h1'],
            partisans=round_db[round_id]['h2'],
            news=round_db[round_id]['h3'],
            hype=round_db[round_id]['h4'],
            cash=round_db[round_id]['h5'],
            media=round_db[round_id]['h6'],
            mojo=round_db[round_id]['h7'],
            money=round_db[round_id]['h8'],
            card_factory=self.card_factory,
            is_bot=False if bot_name == 'trump' else True)

        if bot_name == 'trump':
            self.trump.set_updaters(self.ids, 'trump_player')
        elif bot_name == 'hillary':
            self.hillary.set_updaters(self.ids, 'hillary_player')

        self.trump.set_opponent(self.hillary)
        self.hillary.set_opponent(self.trump)

        # if round_db[round_id]['turn']:
        #     self.trump.set_active(False)
        #     self.hillary.set_active(True)
        # else:
        #     self.trump.set_active(True)
        #     self.hillary.set_active(False)

        if bot_name == 'trump':
            self.trump.set_active(False)
            self.hillary.set_active(True)
        elif bot_name == 'hillary':
            self.trump.set_active(True)
            self.hillary.set_active(False)


        # shuffle Decks
        self.trump.get_deck().shuffle()
        self.hillary.get_deck().shuffle()

        # deal 6 Cards from Decks to Hands
        self.trump.get_hand().refill()
        self.trump.get_hand().render_cards()
        self.hillary.get_hand().refill()
        self.hillary.get_hand().render_cards()

        if round_db[round_id]['turn'] and bot_name == 'hillary':
            self.hillary.play()
        elif not round_db[round_id]['turn'] and bot_name == 'trump':
            self.trump.play()

    def end_game(self, winner_name):
        """Sets both Players to active=False to prevent playing further cards"""
        self.trump.set_active(False)
        self.hillary.set_active(False)
        end_screen = EndScreen(winner_name, name='endscreen')
        self.sm.add_widget(end_screen)
        self.sm.current = 'endscreen'
        print 'END GAME'


    def declare_victory(self):
        """checks if victory is achieved
       !! Current problem - what if both players are hit with one card?"""
        #
        # Use any() function + 2 dictionaries of victory that are updated from card turn
        #
        if self.victory['destr'] == 1:  # destruction is true/false
            # if Trump wins
            if self.hillary.get_voters() <= 0:
                self.trump.set_winner(True)
                print 'Trump won'
                return True, 'Trump'
            # if Hillary wins
            elif self.trump.get_voters() <= 0:
                self.hillary.set_winner(True)
                print 'Hillary won'
                return True, 'Hillary'
            # No winner yet
            else:
                # print 'No winner yet'
                return False, None
        else:
            print 'No victory condition set!'

    def card_clicked(self, card):
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        free_turn = False
        if player.get_active():
            print '\nBegin new turn with player ', self.PLAYERS[card.get_owner()]
            if not player.pay_for_card(*card.get_cost()):
                return False
            player.get_hand().pop_card(card)
            player.get_deck().drop_card(card)  # even played card should be in discard
            if player.is_bot():
                card.show()
            actions = card.get_actions()  # {'player': [(type, value)], 'opponent': [(type, value)]}
            for action in actions['player']:
                if player.apply_card(*action):
                    free_turn = True
            for action in actions['opponent']:
                opponent.apply_card(*action)

            is_victory, winner = self.declare_victory()
            if is_victory:
                self.end_game(winner)
                return True

            if free_turn:
                if player.is_bot():
                    player.get_hand().refill()
                    player.set_active(True)
                else:
                    player.get_hand().refill()
                    player.get_hand().render_cards()
            else:
                player.set_active(False)
                opponent.update_resources()
                player.get_hand().refill()
                opponent.set_active(True)
                opponent.get_hand().render_cards()
                player.get_hand().render_cards()

            return True
        else:
            print 'Its not your turn!'
            return False

    def card_dropped(self, card):
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        if player.get_active():
            player.get_hand().pop_card(card)
            player.get_deck().drop_card(card)
            player.set_active(False)
            player.get_hand().refill()
            opponent.update_resources()
            opponent.set_active(True)
            if opponent.is_bot():
                opponent.play()
                if self.declare_victory():
                    return True
            player.get_hand().render_cards()
            opponent.get_hand().render_cards()
            return True
        return False
