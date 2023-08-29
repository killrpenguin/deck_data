from dataclasses import dataclass
from typing import List

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
import re
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
        pause = randint(5, 15)
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get('https://scryfall.com/')
        driver.implicitly_wait(pause)
        search_box = driver.find_element(By.XPATH, "//html/body/div[@id='main']//div[@class='homepage']"
                                                   "//div[@class='inner-flex']//form[@class='homepage-form']"
                                                   "//input[@id='q']")
        search_box.send_keys(card_name)
        search_box.send_keys(Keys.ENTER)
        try:
            card_details = driver.find_element(By.CLASS_NAME, 'card-text').text.split('\n')
        except NoSuchElementException:
            print(card_name)
        self.card_name = card_details.pop(0)
        self.cmc = card_details.pop(0)
        self.card_type = card_details.pop(0)
        self.legal_status = ''
        self.card_text = []
        for i in range(len(card_details)):
            commander_legal = re.search('^C.+', card_details[i])
            if commander_legal is not None:
                self.legal_status = card_details[i + 1]
        for string in card_details:
            artist = re.search('^Ill.+', string)
            if artist is not None:
                break
            self.card_text.append(string)
        driver.close()