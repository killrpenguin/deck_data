from dataclasses import dataclass
from typing import List
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.keys import Keys
from random import randint


@dataclass()
class Card():
    card_name: str
    cmc: str
    card_type: str
    card_text: List
    legal_status: str


    def populate_card_info(self, card_name, proxy):
        pause = randint(5, 15)
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('headless')
        edge_options.add_argument('disable-gpu')
        edge_options.add_argument("--proxy_server=%s" % proxy)
        driver = selenium.webdriver.Edge(options=edge_options)
        driver.get('https://scryfall.com/')
        driver.implicitly_wait(pause)
        search_box = driver.find_element(By.XPATH, "//html/body/div[@id='main']//div[@class='homepage']"
                                                   "//div[@class='inner-flex']//form[@class='homepage-form']"
                                                   "//input[@id='q']")
        search_box.send_keys(card_name)
        search_box.send_keys(Keys.ENTER)
        card_details = driver.find_element(By.CLASS_NAME, 'card-text').text.split('\n')
        self.card_name = card_details.pop(0)
        self.cmc = card_details.pop(0)
        self.card_type = card_details.pop(0)

        driver.close()
