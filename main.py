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


link = "https://archidekt.com/decks/86888"

proxy = 'http://24.158.29.166:80'
testing = Decks()

testing.mk_deck_objs()

"""name_xpath = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]"
author_xpath = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div/div[1]/div[2]/div[1]/div[1]/a"
deck_xpath = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div/div[2]/div[2]/div"
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
edge_options.add_argument("--proxy_server=%s" % proxy)
driver = selenium.webdriver.Edge(options=edge_options)
driver.get(link)
wait = WebDriverWait(driver, 20)
name = wait.until(ec.presence_of_element_located((By.XPATH, name_xpath))).text
author = wait.until(ec.presence_of_element_located((By.XPATH, author_xpath))).text
deck = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text
print(f"{name}, {author}, {deck}")
driver.close()
"""
