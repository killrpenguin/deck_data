from bs4 import BeautifulSoup as bs
from scraper_targets import Scraper_Targets
import requests
import re


def ddb_objects():
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    f = open('competitive_decks', 'r').read().strip().split('\n')
    project_href = [spi['href'] for spi in soup.find_all('a', href=True)]
    # regex removes any href with the word discord, scryfall, docs and anything that starts with a /
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