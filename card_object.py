from dataclasses import dataclass
from typing import List
from typing import Dict
import time
import json
import requests
from bs4 import BeautifulSoup


@dataclass()
class Card:
    card_name: str
    mc: str
    card_type: str
    card_text: List
    legal_status: str
    card_layout: str
    json : Dict


    def print_card_details(self):
        print(f'{self.card_name}, {self.mc}, {self.card_type}, {self.legal_status}, {self.card_text}')


    # REMEMBER TO LIMIT TO < 10 REQUESTS PER SECOND
    def populate_with_api(self, card):
        link = "https://api.scryfall.com/cards/named?fuzzy=" + card
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        self.card_dict = json.loads(soup.text)
        self.card_layout = self.card_dict['layout']
        try:
            if self.card_dict['layout'] == 'normal':
                self.card_name = self.card_dict['name']
                self.mc = self.card_dict['mana_cost']
                self.card_type = self.card_dict['type_line']
                self.card_text = self.card_dict['oracle_text'].split('\n')
                self.legal_status = self.card_dict['legalities']['commander']
            elif self.card_dict['layout'] == 'modal_dfc':
                self.card_name = f"Front: {self.card_dict['card_faces'][0]['name']} Back: {self.card_dict['card_faces'][1]['name']}"
                self.mc = f"Front: {self.card_dict['card_faces'][0]['mana_cost']} Back: {self.card_dict['card_faces'][1]['mana_cost']}"
                self.card_type = self.card_dict['type_line']
                self.card_text = self.card_dict['card_faces'][0]['oracle_text'].split('\n')
                self.card_text = ["Front: " + text for text in self.card_text]
                back = self.card_dict['card_faces'][1]['oracle_text'].split('\n')
                for text in back:
                    self.card_text.append("Back: " + text)
                self.legal_status = self.card_dict['legalities']['commander']
        except Exception as e:
            print(self.card_dict['name'])
            print(e)


        time.sleep(.25)


"""card = Card('', '', '', [], '')
proxy = 'http://45.225.184.177:999'
card.populate_with_api('Mountain')
print(f'{card.card_name}, {card.card_type}, {card.card_text}, {card.mc}, {card.legal_status}')
"""