from dataclasses import dataclass, field
from typing import Dict
import time
import json
import requests
from bs4 import BeautifulSoup


@dataclass
class Face:
    face_name: str = field(default=str)
    cmc: float = field(default=float)
    mana_cost: str = field(default=str)
    card_type: str = field(default=str)
    card_text: str = field(default=str)
    color_ident: str = field(default=str)


class Card():
    def __init__(self, card_name):
        self.card_name = card_name
        self.card_dict = self.get_json_dict(self.card_name)
        self.card_layout = self.card_dict['layout']
        self.faces = self.make_faces(self.card_dict)
        self.legal_status = self.card_dict['legalities']['commander']

    def get_json_dict(self, card) -> Dict:
        link = "https://api.scryfall.com/cards/named?fuzzy=" + card
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        card_dict = json.loads(soup.text)
        time.sleep(.25)
        return card_dict

    def make_faces(self, card) -> list:
        faces = []
        try:
            for side in range(len(card['card_faces'])):
                faces.append(Face(face_name=card['card_faces'][side]['name'],
                                  cmc=card['cmc'], mana_cost=card['card_faces'][side]['mana_cost'],
                                  card_type=card['card_faces'][side]['type_line'],
                                  card_text=card['card_faces'][side]['oracle_text']))
        except KeyError:
            faces.append(Face(face_name=card['name'], cmc=card['cmc'], mana_cost=card['mana_cost'],
                              card_type=card['type_line'], card_text=card['oracle_text']
                              ))
        return faces
