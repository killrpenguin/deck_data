from bs4 import BeautifulSoup as bs
from scraper_targets import Scraper_Targets
import requests
import re


def ddb_objects():
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    f = open('competitive_decks', 'r').read().strip().split('\n')
    project_href = [element['href'] for element in soup.find_all('a', href=True)]
    # regex removes any href with the word discord, scryfall, docs and anything that starts with a /
    project_href = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', href) for href in project_href]
    project_href = [href.strip() for href in project_href if '' != href if '/' != href]
    deck_objects = []
    for link in project_href:
        site = re.sub(".+www\.|\.c.+|.n.+|^ht.+?//|\.o.+", '', link)
        if link in f:
            st = Scraper_Targets(deck_link=link, link_group=site, category='Competitive')
        else:
            st =Scraper_Targets(deck_link=link, link_group=site, category='Outdated')
        deck_objects.append(st)
    return deck_objects