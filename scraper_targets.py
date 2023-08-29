from bs4 import BeautifulSoup as bs
import requests
import random
from selenium.webdriver.common.by import By
import re
import helper_functions


class Scraper_Targets():
    def __init__(self, deck_link, link_group=None, category=None, deck_commander=None):
        self.wait = random.randint(5, 15)
        self.deck_link = deck_link # URL
        self.link_group = link_group # ex: This will define which scraper function to use. Moxfield, tappedout, etc.
        self.category = category # competitive or outdated from ddb grouping
        self.deck_name = str
        self.deck_commander = deck_commander # Populate later
        self.deck_author = []
        self.deck_list = []

    def get_mx(self, proxy):
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get(self.deck_link)
        driver.implicitly_wait(self.wait)
        self.deck_author = driver.find_element(By.XPATH, "//div[@class='container py-5 text-white']"
                                                         "//div[@class='mb-3']//div[@class='d-flex align-items-center']"
                                                         "//div[@class='flex-grow-1']"
                                                         "//div[@class='h3 d-flex flex-wrap align-items-center']").text.split(',')
        self.deck_author = [i.strip() for i in self.deck_author]
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
                           "^V.+\sO.+|^A..\sT.+|\.|^T.+\sLa.+\sE.+", '', a) for a in decklist]
        self.deck_list = [a.strip() for a in decklist if '' != a]
        driver.close()


    def get_tp(self, proxy):
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get(self.deck_link)
        driver.implicitly_wait(self.wait)
        self.deck_name = driver.find_element(By.XPATH, "//body[@id='sitebody']"
                                                  "//div[@id='main-content']"
                                                  "//div[@id='body']"
                                                  "//div[@class='container-fluid']"
                                                  "//div[@class='row']"
                                                  "//div[@class='col-lg-9 col-md-8']"
                                                  "//div[@class='row'][1]//div[@class='col-xs-12']"
                                                  "//div[@class='well well-jumbotron']/h2")
        decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='row board-container'][1]//descendant::div")
        decklist = [a.text.strip().split('\n') for a in decklist_dirty]
        decklist = [a for b in decklist for a in b]
        decklist = [re.sub("^[0-9]x|[1-9][0-9]x", '', a) for a in decklist]
        self.deck_list = [a.strip() for a in decklist if a if '(' not in a]
        driver.close()


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