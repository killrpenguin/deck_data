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
    legal_status: str
    card_layout: str
    face : self.store_faces()
    json : Dict

    def store_faces(self):
        self.face.append(face()

class face(Card):
    mc: str
    card_type: str
    card_text: List
    color_ident : str
