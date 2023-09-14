from deck_scraper import (Decks, Deck, Card, Face)
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from helper_functions import web_driver
import selenium
from selenium.webdriver import EdgeOptions
import re

link = "https://tappedout.net/mtg-decks/26-04-19-zada-storm/"

proxy = 'http://24.158.29.166:80'
testing = Decks()
for i in testing.deck_list_database:
    if ('moxfield' not in i) or ('tappedout' not in i):
        print(i)
"""name_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[1]/div/div/h2"
author_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[1]/div/div/p[2]/a"
deck_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[2]/div[2]/div[1]/div[2]"
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get(link)
wait = WebDriverWait(driver, 20)

driver.close()
"""