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
        print(f'{self.card_name}, {self.cmc}, {self.card_type}, {self.legal_status}, {self.card_text}')

    def populate_card_info(self, card_name, proxy):
        xpath_card_name = "/html/body/div[3]/div[1]/div/div[3]/h1/span[1]"
        xpath_card_type = "/html/body/div[3]/div[1]/div/div[3]/p[1]"
        xpath_cmc = "/html/body/div[3]/div[1]/div/div[3]/h1/span[2]/abbr"
        xpath_legal_status = "/html/body/div[3]/div[1]/div/div[3]/dl/div[6]/div[1]"
        xpath_card_text = "/html/body/div[3]/div[1]/div/div[3]/div"
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
        self.card_name = wait.until(ec.presence_of_element_located((By.XPATH, xpath_card_name))).text
        self.card_type = wait.until(ec.presence_of_element_located((By.XPATH, xpath_card_type))).text
        self.cmc = wait.until(ec.presence_of_element_located((By.XPATH, xpath_cmc))).text
        self.legal_status = wait.until(ec.presence_of_element_located((By.XPATH, xpath_legal_status))).text
        self.card_text = wait.until(ec.presence_of_element_located((By.XPATH, xpath_card_text))).text
        driver.close()

"""
card = Card('', '', '', [], '')
proxy = 'http://45.225.184.177:999'
card.populate_card_info('Mana Crypt', proxy)
# print(f'{card.card_name}, {card.card_type}, {card.card_text}, {card.cmc}, {card.legal_status}')
"""