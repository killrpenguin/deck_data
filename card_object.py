from dataclasses import dataclass
from typing import List

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
        pause = randint(5, 12)
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get('https://scryfall.com/')
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=pause, poll_frequency=.2, ignored_exceptions=errors)
        search_box = driver.find_element(By.XPATH, "//html/body/div[@id='main']//div[@class='homepage']"
                                                   "//div[@class='inner-flex']//form[@class='homepage-form']"
                                                   "//input[@id='q']")
        search_box.send_keys(card_name)
        search_box.send_keys(Keys.ENTER)
        card_name = driver.find_element(By.XPATH, "//html//body//div[@id='main']//div[@class='card-profile']"
                                                       "//div[@class='inner-flex']//div[@class='card-text']"
                                                       "//h1[@class='card-text-title']"
                                                       "//span[@class='card-text-card-name']").text
        wait.until(lambda d : card_name.is_displayed())
        self.card_name = card_name
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


card = Card('', '', '', [], '')
proxy = 'http://45.225.184.177:999'
card.populate_card_info('Mana Crypt', proxy)
print(f'{card.card_name}, {card.card_type}, {card.card_text}, {card.cmc}, {card.legal_status}')
