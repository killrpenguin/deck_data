# change to data class

class Card():
    def __init__(self, card_name, card_type=None, cmc=None, color_identity=None):
        self.card_name = card_name
        self.card_type = card_type
        self.cmc = cmc
        self.color_identity = color_identity
