from scraper_targets import Scraper_Targets
from bs4 import BeautifulSoup as bs
import requests
import re

def scraper():
    url = "https://cedh-decklist-database.com/"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    f = open('competitive_decks', 'r')
    project_href = [spi['href'] for spi in soup.find_all('a', href=True)]
    project_href = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', i) for i in project_href]
    project_href = [i.strip() for i in project_href if '' != i if '/' != i]
    link_objects = [Scraper_Targets(link) for link in project_href]




if __name__ == '__main__':
    scraper()