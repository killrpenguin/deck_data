from scraper_targets import Scraper_Targets
from bs4 import BeautifulSoup
import requests
import re


class Deck(scraper_targets):
    def __init__(self, deck_link, link_group, category,
                 deck_name, deck_author=None, commander=None):
        super().__init__(deck_link, link_group, category)
        self.deck_name = deck_name
        self.deck_commander = commander
        self.deck_author = deck_author
        self.deck_list = set()


class Card():
    def __init__(self, card_name, card_type=None, cmc=None, color_identity=None):
        self.card_name = card_name
        self.card_type = card_type
        self.cmc = cmc
        self.color_identity = color_identity
