from scraper_targets import Scraper_Targets
from selenium.webdriver.common.by import By
import helper_functions
import re
import selenium


class Deck(Scraper_Targets):
    def __init__(self, deck_link, link_group, category,
                 driver, deck_author=None, commander=None):
        super().__init__(deck_link, link_group, category)
        # use selenium webdriver and xpath to find the name of a deck on moxfield
        self.deck_name = driver.find_element(By.XPATH, "/span[@id='menu-deckname']/span[@class='deckheader-name']")
        self.deck_commander = commander
        self.deck_author = deck_author
        self.deck_list = driver.find_elements(By.XPATH, "//div[@class='deckview']")


    def clean_moxfield(self):
        self.deck_list = [a.text.strip().split('\n') for a in self.deck_list]
        self.deck_list = [a for a in self.deck_list[0]]
        decklist = [re.sub("^\d*x|[A-Za-z]/[A-Za-z]|^\$.+|^€.+|.+\(\d+.*|"
                           "[0-9]|^R.+\sH.+|^[A-Za-z].+@.[A-Za-z].+|"
                           "^V.+\sO.+|^A..\sT.+", '', a) for a in self.deck_list]
        self.deck_list = [a.strip() for a in decklist if '' != a]
        return self.deck_list
