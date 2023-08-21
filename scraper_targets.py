import random


class scraper_targets():
    def __init__(self, deck_link, link_group, category):
        self.wait = random.randint(5, 15)
        self.deck_link = deck_link # URL
        self.link_group = link_group # ex: moxfield, tappedout, deckstats, arkedekt
        self.category = category # competitive or outdated from ddb grouping
        self.deck = {}



class Card():
    def __init__(self, card_name, card_type=None, cmc=None, color_identity=None):
        self.card_name = card_name
        self.card_type = card_type
        self.cmc = cmc
        self.color_identity = color_identity
