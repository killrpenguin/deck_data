from bs4 import BeautifulSoup as bs
import requests
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
import re



class Scraper_Targets():
    def __init__(self, deck_link, link_group=None, category=None, deck_commander=None, deck_author=None):
        self.wait = random.randint(5, 15)
        self.deck_link = deck_link # URL
        self.link_group = link_group # ex: This will define which scraper function to use. Moxfield, tappedout, etc.
        self.category = category # competitive or outdated from ddb grouping
        self.deck_list = []
        self.deck_name = ''
        self.deck_commander = deck_commander
        self.deck_author = deck_author

    def get_mx(self, proxy):
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
        edge_options.add_argument("--proxy_server=%s" % proxy)
        driver = selenium.webdriver.Edge(options=edge_options)
        driver.get(self.deck_link)
        driver.implicitly_wait(self.wait)
        self.deck_name = driver.find_element(By.XPATH, "//div[@class='deckheader']"
                                                  "//div[@class='deckheader-content']/"
                                                  "/div[@class='container py-5 text-white']"
                                                  "//form/h1[@class='mb-2']/"
                                                  "/span[@id='menu-deckname']"
                                                  "//span[@class='deckheader-name']").text
        decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='deckview']")
        decklist = [a.text.strip().split('\n') for a in decklist_dirty]
        decklist = [a for a in decklist[0]]
        decklist = [re.sub("^\d*x|[A-Za-z]/[A-Za-z]|^\$.+|^€.+|.+\(\d+.*|"
                           "[0-9]|^R.+\sH.+|^[A-Za-z].+@.[A-Za-z].+|"
                           "^V.+\sO.+|^A..\sT.+", '', a) for a in decklist]
        self.deck_list = [a.strip() for a in decklist if '' != a]



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