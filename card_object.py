from dataclasses import dataclass
from typing import List
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
from selenium.webdriver.support.wait import WebDriverWait

import helper_functions


@dataclass()
class Card:
    card_name: str
    cmc: str
    card_type: str
    card_text: List
    legal_status: str


    def print_card_details(self):
        pass

    def populate_card_info(self, card_name, proxy):
        pause = randint(1, 4)
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get('https://scryfall.com/')
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=pause, poll_frequency=.2, ignored_exceptions=errors)
        search_box = driver.find_element(By.XPATH, "//html/body/div[@id='main']//div[@class='homepage']"
                                                   "//div[@class='inner-flex']//form[@class='homepage-form']"
                                                   "//input[@id='q']")
        search_box.send_keys(card_name)
        search_box.send_keys(Keys.ENTER)
        self.card_name = wait.until(ec.presence_of_element_located((By.XPATH, "//h1[@class='card-text-title']//child::span"))).text
        self.card_type = wait.until(ec.presence_of_element_located(((By.CLASS_NAME, "card-text-type-line")))).text
        self.cmc = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'card-text-mana-cost'))).text
        self.legal_status = wait.until(ec.presence_of_element_located((By.XPATH, ""))).text
        print(self.card_name)
        print(self.card_type)
        print(self.cmc)
        print(self.legal_status)
        driver.close()


card = Card('', '', '', [], '')
proxy = 'http://45.225.184.177:999'
card.populate_card_info('Mana Crypt', proxy)
# print(f'{card.card_name}, {card.card_type}, {card.card_text}, {card.cmc}, {card.legal_status}')
