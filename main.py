from deck_scraper import (Decks, Deck, Card, Face)
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from helper_functions import web_driver
import re


deck_objects_list = []
proxy = 'http://24.158.29.166:80'
testing = Decks()
for link in testing.deck_list_database:
    deck_obj = Deck(deck_link=link, proxy=proxy)
    deck_objects_list.append(deck_obj)
    print(f"{deck_obj.deck_name}, {deck_obj.deck_author} {len(deck_obj.deck_list)}")