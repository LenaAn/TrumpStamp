import kivy
import pandas as pd
from kivy.uix.floatlayout import FloatLayout
from card import Card, CardFabric
from kivy.logger import Logger
import random
kivy.require('1.7.2')


class Deck():
	
	def __init__(self, player, card_fabric):
		self.player = player
		self.cards = [card_fabric.get_card(i, player.get_player_id()) for i in xrange(1, 54)]

	def shuffle(self):
		random.shuffle(self.cards)