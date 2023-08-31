import random
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import re

from selenium.webdriver.support.wait import WebDriverWait

import helper_functions


class Scraper_Targets():
    def __init__(self, deck_link, link_group=None, category=None, deck_commander=None):
        self.wait = random.randint(1, 3)
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
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=self.wait, poll_frequency=.2, ignored_exceptions=errors)
        self.deck_author = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='container py-5 text-white']"
                                                         "//div[@class='mb-3']//div[@class='d-flex align-items-center']"
                                                         "//div[@class='flex-grow-1']"
                                                         "//div[@class='h3 d-flex flex-wrap align-items-center']"))).text.split(',')
        self.deck_author = [name.strip() for name in self.deck_author]
        self.deck_name = wait.until(ec.presence_of_element_located((By.XPATH, """/div[@class='deckheader']
        /div[@class='deckheader-content']/div[@class='container py-5 text-white']
        /form/h1[@class='mb-2']/span[@id='menu-deckname']/span[@class='deckheader-name']"""))).text
        decklist_dirty = wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class='deckview]")))
        decklist = [card.text.strip().split('\n') for card in decklist_dirty]
        decklist = [card for card in decklist[0]]
        decklist = [re.sub("^\d*x|[A-Za-z]/[A-Za-z]|^\$.+|^€.+|.+\(\d+.*|"
                           "[0-9]|^R.+\sH.+|^[A-Za-z].+@.[A-Za-z].+|"
                           "^V.+\sO.+|^A..\sT.+|\.|^T.+\sLa.+\sE.+", '', card) for card in decklist]
        self.deck_list = [card.strip() for card in decklist if '' != card]
        driver.close()


    def get_tp(self, proxy):
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get(self.deck_link)
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=self.wait, poll_frequency=.2, ignored_exceptions=errors)
        wait.until(lambda d : decklist_dirty.is_displayed())
        self.deck_name = driver.find_element(By.XPATH, "//body[@id='sitebody']"
                                                  "//div[@id='main-content']"
                                                  "//div[@id='body']"
                                                  "//div[@class='container-fluid']"
                                                  "//div[@class='row']"
                                                  "//div[@class='col-lg-9 col-md-8']"
                                                  "//div[@class='row'][1]//div[@class='col-xs-12']"
                                                  "//div[@class='well well-jumbotron']/h2")
        decklist_dirty = driver.find_elements(By.XPATH, "//div[@class='row board-container'][1]//descendant::div")
        decklist = [card.text.strip().split('\n') for card in decklist_dirty]
        decklist = [section_a for section_b in decklist for section_a in section_b]
        decklist = [re.sub("^[0-9]x|[1-9][0-9]x", '', card) for card in decklist]
        self.deck_list = [card.strip() for card in decklist if card if '(' not in card]
        driver.close()


