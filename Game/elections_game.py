# coding=utf-8
"""Game logic module."""
import kivy
import os
import csv
from urllib import urlencode
from urllib2 import urlopen
from collections import defaultdict
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from card import CardFactory
from kivy.animation import Animation
from player import Player
from base_screen import BaseScreen
import end_screen
import menu
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from bots import *
import tracker

kivy.require('1.7.2')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

round_csv = os.path.join(SCRIPT_DIR, 'rounds538.csv')
cards_csv = os.path.join(SCRIPT_DIR, 'cards.csv')


class ElectionsGame(BaseScreen):
    """
       This class represents the game.

    As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """

    def __init__(self, sm, **kwargs):
        """Init game."""
        super(ElectionsGame, self).__init__(**kwargs)
        self.card_factory = None
        self.sm = sm
        self.menu_icon = self.ids['Menu']
        self.menu_screen = None
        self.trump = None
        self.hillary = None
        self.bot_name = None
        self.store = None
        self.round_id = None
        self.state = None
        self.area = None
        self.card_counter_hillary = 0
        self.card_counter_trump = 0

    def set_store(self, store):
        self.store = store

    def set_start_screen(self, menu_screen):
        self.menu_screen = menu_screen
        print('SEEEEETTTT STAAART SCREEEEn')

    def set_bot(self, bot_name):
        """Set bot player."""
        print(self.bot_name, bot_name)
        self.bot_name = bot_name
        if bot_name == 'trump':
            self.trump = RandomPressBot(self.ids['trump_player'])
            self.hillary = self.ids['hillary_player']
        elif bot_name == 'hillary':
            self.hillary = RandomPressBot(self.ids['hillary_player'])
            self.trump = self.ids['trump_player']

        self.PLAYERS = {0: self.trump,
                        1: self.hillary}

    def get_bot(self):
        return 1 if self.bot_name == 'hillary' else 0

    def set_round(self, round_id, state, area):
        self.round_id = round_id
        self.state = state
        self.area = area
        round_db = []
        with open(round_csv) as round_file:
            reader = csv.DictReader(round_file)
            for row in reader:
                row_ = {k: int(v) for k, v in row.iteritems()}
                round_db.append(row_)

        self.victory = {'destr': round_db[round_id]['destr'], 'res': round_db[round_id]['res']}
        # CREATE PLAYERS
        # parameters are labeled as t0-t1, digit points to resource code per card database
        #cards = CardFactory(None, os.path.join(SCRIPT_DIR, 'cards.csv'))
        self.card_factory = CardFactory(self, cards_csv)

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
            state_area= str(area + ',   ' + state),
            is_bot=False if self.bot_name == 'hillary' else True)
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
            state_area= str(area + ',   ' + state),
            is_bot=False if self.bot_name == 'trump' else True)

        if self.bot_name == 'trump':
            self.trump.set_updaters(self.ids, 'trump_player')
        elif self.bot_name == 'hillary':
            self.hillary.set_updaters(self.ids, 'hillary_player')

        self.trump.set_opponent(self.hillary)
        self.hillary.set_opponent(self.trump)

        if self.bot_name == 'trump':
            self.trump.set_active(False)
            self.hillary.set_active(True)
        elif self.bot_name == 'hillary':
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

        if round_db[round_id]['turn'] and self.bot_name == 'hillary':
            self.hillary.play()
        elif not round_db[round_id]['turn'] and self.bot_name == 'trump':
            self.trump.play()

    def end_game(self, winner_name):
        """Set both Players to active=False to prevent playing further cards."""
        self.trump.set_active(False)
        self.hillary.set_active(False)
        end_screen_ = end_screen.EndScreen(self.sm, bot=self.bot_name, winner=winner_name,
                                           round=self.round_id, store=self.store,
                                           area=self.area, state=self.state,
                                           menu_screen=self.menu_screen, name='endscreen')
        self.sm.switch_to(end_screen_, duration=.5)

    def declare_victory(self):
        """Check if victory is achieved.

        !! Current problem - what if both players are hit with one card?
        """
        #
        # Use any() function + 2 dictionaries of victory that are updated from card turn
        #
        if self.victory['destr'] == 1:  # destruction is true/false
            # if Trump wins
            if self.hillary.get_voters() <= 0:
                self.trump.set_winner(True)
                return True, 'Trump'
            # if Hillary wins
            elif self.trump.get_voters() <= 0:
                self.hillary.set_winner(True)
                return True, 'Hillary'
            # No winner yet
            else:
                # print 'No winner yet'
                return False, None
        else:
            print 'No victory condition set!'

    def get_updated_counter(self, card):
        if card.get_owner():
            self.card_counter_trump += 1
            return self.card_counter_trump
        else:
            self.card_counter_hillary += 1
            return self.card_counter_hillary

    def card_clicked(self, card):
        """Card click callback."""
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        free_turn = False
        if player.get_active() and player.hand.card_in_hand(card):
            #print '\nBegin new turn with player ', self.PLAYERS[card.get_owner()]
            if not player.is_bot():
                tracker.tracker.send(tracker.EventBuilder().set(ec="user action",
                                                                ea="clicked card {}".format(repr(card))).build())
            if not player.pay_for_card(*card.get_cost()):
                return False, None
            player.get_hand().pop_card(card)
            if player.is_bot():
                card.show()
            actions = card.get_actions()
            for action in actions['player']:
                if player.apply_card(*action):
                    free_turn = True
            for action in actions['opponent']:
                opponent.apply_card(*action)

            is_victory, winner = self.declare_victory()
            if is_victory:
                if player.player_name[0] == winner.lower()[0]:
                    winner_obj = player
                else:
                    winner_obj = opponent
                bot_str = 'bot' if winner_obj.is_bot() else 'player'
                tracker.tracker.send(tracker.EventBuilder().set(ec="victory",
                                                                ea="{} ({}) won".format(winner, bot_str)).build())
                self.end_game(winner)
                return True, self.get_updated_counter(card)

            if free_turn:
                card.set_free_turn(True)
                if player.is_bot():
                    player.get_hand().refill()
                    player.get_hand().render_cards()
                    player.set_active(True)
                else:
                    player.get_hand().refill()
                    player.get_hand().render_cards()
            else:
                player.set_active(False)
                opponent.update_resources()
                player.get_hand().refill()
                player.get_hand().render_cards()
                opponent.set_active(True)
                if not opponent.is_bot():
                    opponent.get_hand().render_cards(just_turn=True)

            return True, self.get_updated_counter(card)
        else:
            #print 'IT IS NOT YOUR TURN!!!!'
            return False, None

    def card_dropped(self, card):
        """Card drop callback."""
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        if player.get_active() and player.hand.card_in_hand(card):
            if not player.is_bot():
                tracker.tracker.send(tracker.EventBuilder().set(ec="user action",
                                                                ea="drop card {}".format(repr(card))).build())
            player.get_hand().pop_card(card)
            player.set_active(False)
            player.get_hand().refill()
            opponent.update_resources()
            player.get_hand().render_cards()
            opponent.set_active(True)
            if not opponent.is_bot():
                opponent.get_hand().render_cards(just_turn=True)
            is_victory, winner = self.declare_victory()
            if is_victory:
                self.end_game(winner)
                return True
            return True
        return False
