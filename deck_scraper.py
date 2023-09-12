import random
import re
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import helper_functions
from bs4 import BeautifulSoup as bs
from scraper_targets import Scraper_Targets
import requests
import re


class Decks():
    def __init__(self):
        self.deck_list_database = self.get_ddb_list()
        self.decks = []

    def get_ddb_list(self) -> list:
        url = "https://cedh-decklist-database.com/"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        deck_hrefs = [element['href'] for element in soup.find_all('a', href=True)]
        # regex removes any href with the word discord, scryfall, docs and anything that starts with a /
        deck_hrefs = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', href) for href in deck_hrefs]
        deck_hrefs = [href.strip() for href in deck_hrefs if '' != href if '/' != href]
        return deck_hrefs

    def disp_obj_data(self) -> list:
        for link in self.deck_list_database:
            deck = Deck(deck_link=link)
            print(f"Link: {deck.deck_link}, Group: {deck.link_group}, Host: {deck.deck_hosted_on}")
            self.decks.append(deck)
        return self.decks

class Deck():
    def __init__(self, deck_link):
        self.deck_link = deck_link
        self.link_group = self.sort_links()
        self.deck_hosted_on = self.sort_hosts()

    def sort_links(self) -> str:
        f = open('competitive_decks', 'r')
        file = f.read().strip().split('\n')
        if self.deck_link in file:
            self.link_group = "Competitive"
        else:
            self.link_group = "Outdated"
        f.close()
        return self.link_group

    def sort_hosts(self) -> str:
        # regex strips everything out of the given weblink to identify which deck website hosts the data.
        self.deck_hosted_on = re.sub(".+www\.|\.c.+|.n.+|^ht.+?//|\.o.+", '', self.deck_link)
        return self.deck_hosted_on