import deck_objects
from bs4 import BeautifulSoup
import requests
import re

f = open('competitive_decks', 'r').read().strip().split('\n')
url = "https://cedh-decklist-database.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
project_href = [spi['href'] for spi in soup.find_all('a', href=True)]
# regex removes web links with the words discord, scryfall and docs along with /word list items
project_href = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', i) for i in project_href]
project_href = [i.strip() for i in project_href if '' != i if '/' != i]
moxfield = set([i for i in project_href if 'moxfield' in i])
tappedout = set([i for i in project_href if 'tappedout' in i])
arkdect = set([i for i in project_href if 'archidekt' in i])
deckstats = set([i for i in project_href if 'deckstats' in i])
deckbox = set([i for i in project_href if 'deckbox' in i])

deck_links = {'mx': moxfield,'tp': tappedout, 'ar': arkdect, 'ds': deckstats, 'db': deckbox}
for i in deck_links
for i in project_href:
    if i in f:
        deck_links[i] = "Competitive"
    else:
        deck_links[i] = "Outdated"