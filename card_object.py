from dataclasses import dataclass
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
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
        search_box = driver.find_element(By.XPATH, "//html/body/div[@id='main']//div[@class='homepage']"
                                                   "//div[@class='inner-flex']//form[@class='homepage-form']"
                                                   "//input[@id='q']")
        search_box.send_keys(card_name)
        search_box.send_keys(Keys.ENTER)
        driver.implicitly_wait(pause)
        self.card_name = driver.find_element(By.XPATH, "//html//body//div[@id='main']//div[@class='card-profile']"
                                                       "//div[@class='inner-flex']//div[@class='card-text']"
                                                       "//h1[@class='card-text-title']"
                                                       "//span[@class='card-text-card-name']").text
        self.cmc = driver.find_element(By.XPATH, "//div[@class='card-text']"
                                                 "//h1[@class='card-text-title']"
                                                 "//span[@class='card-text-mana-cost']").text
        self.card_type = driver.find_element(By.XPATH, "//div[@class='card-text']"
                                                       "//p[@class='card-text-type-line']").text
        self.legal_status = driver.find_element(By.XPATH, "//div[@class='card-text']"
                                                          "//dl[@class='card-legality']"
                                                          "//div[@class='card-legality-row'][6]/"
                                                          "/div[@class='card-legality-item'][1]").text
        self.card_text = driver.find_element(By.XPATH, "//div[@class='card-text']"
                                                       "//div[@class='card-text-box']").text
        driver.close()

"""
card = Card('Mana Crypt', '', '', [], '')
proxy = 'http://45.225.184.177:999'
card.populate_card_info(card.card_name, proxy)
print(f'{card.card_name}, {card.card_type}, {card.card_text}, {card.cmc}, {card.legal_status}')
"""