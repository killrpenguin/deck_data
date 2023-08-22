from bs4 import BeautifulSoup as bs
import requests
import random
import re


class Scraper_Targets():
    def __init__(self, deck_link, link_group=None, category=None):
        self.wait = random.randint(5, 15)
        self.deck_link = deck_link # URL
        self.link_group = link_group # ex: moxfield, tappedout, deckstats, arkedekt
        self.category = category # competitive or outdated from ddb grouping


def ddb_objects():
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    f = open('competitive_decks', 'r').read().strip().split('\n')
    project_href = [spi['href'] for spi in soup.find_all('a', href=True)]
    project_href = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', i) for i in project_href]
    project_href = [i.strip() for i in project_href if '' != i if '/' != i]
    deck_objects = []
    for i in project_href:
        site = re.sub(".+www\.|\.c.+|.n.+|^ht.+?//|\.o.+", '', i)
        if i in f:
            st = Scraper_Targets(deck_link=i, link_group=site, category='Competitive')
        else:
            st =Scraper_Targets(deck_link=i, link_group=site, category='Outdated')
        deck_objects.append(st)
    return deck_objects