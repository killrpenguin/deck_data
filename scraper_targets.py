import random
import re
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import helper_functions


class Scraper_Targets():
    def __init__(self, deck_link, link_group=None, category=None, deck_commander=None):
        self.wait = random.randint(5, 15)
        self.deck_link = deck_link # URL
        self.link_group = link_group # ex: This will define which scraper function to use. Moxfield, tappedout, etc.
        self.category = category # competitive or outdated from ddb grouping
        self.deck_name = str
        self.deck_commander = deck_commander
        self.deck_author = []
        self.deck_list = []

    def get_mx(self, proxy):
        deck_xpath = """/html/body/div[1]/main/div[8]/div[1]/div[2]/div[1]"""
        author_xpath = """/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[1]/div/div[2]/div/span/a"""
        name_xpath = """/html/body/div[1]/main/div[3]/div[2]/div[1]/div/form/h1/span/span"""
        driver = helper_functions.web_driver(proxy=proxy)
        driver.get(self.deck_link)
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(driver, timeout=30, poll_frequency=.2, ignored_exceptions=errors)
        self.deck_author = wait.until(ec.presence_of_element_located((By.XPATH, author_xpath))).text.split(',')
        self.deck_author = [name.strip() for name in self.deck_author]
        self.deck_name = wait.until(ec.presence_of_element_located((By.XPATH, name_xpath))).text
        # fix the next 3 lines later.
        # commander_string = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.replace('\n', '')
        # regex returns the string between grouping 1 Example= 'r(num)num' and grouping 2 Example='Ba(num)
        # self.deck_commander = re.search("(?<=r\(\d\)\d).*?(?=Ba.+\(\d\))", commander_string).group()
        self.deck_list = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.split('\n')
        # regex replaces all numbers, and the 9 card type catagories from each list with ''
        self.deck_list = [
            re.sub("^[0-9]|^[0-9][0-9]|^C.+(.)|^A.+(.)|^E.+(.)|^B.+(.)|^P.+(.)|^I.+(.)|^S.+(.)|^L.+(.)", '', card) for
            card in self.deck_list]
        self.deck_list = [card.strip() for card in self.deck_list if '' != card]
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


