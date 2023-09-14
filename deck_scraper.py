import requests
import re
import asyncio
import proxy_pool
import selenium
import asyncio
import aiohttp
from dataclasses import dataclass, field
from typing import Dict, List
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from proxy_pool import main_proxy_pool
from selenium import webdriver
from selenium.webdriver import EdgeOptions


class Decks:
    def __init__(self):
        self.deck_list_database = self.get_ddb_list()
        self.proxies = 'http://24.158.29.166:80'
        # self.proxies = proxy_pool.asyncio.run(main_proxy_pool())
        self.decks = []

    def get_ddb_list(self) -> list:
        url = "https://cedh-decklist-database.com/"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        deck_hrefs = [element['href'] for element in soup.find_all('a', href=True)]
        # regex removes any href with the word discord, scryfall, docs and anything that starts with a /
        deck_hrefs = [re.sub('^/.+|.+discord.+|.+scryfall.+|.+docs.+|', '', href) for href in deck_hrefs]
        deck_hrefs = [href.strip() for href in deck_hrefs if '' != href if '/' != href]
        return deck_hrefs

    def mk_deck_objs(self) -> list:
        for link in self.deck_list_database:
            deck = Deck(deck_link=link, proxy=self.proxies)
            print(f"Link: {deck.deck_link}, Group: {deck.link_group}, Host: {deck.deck_hosted_on}")
            print(f"Name: {deck.deck_name}, Deck: {len(deck.deck_list)} Author: {deck.deck_author}")
            self.decks.append(deck)
        return self.decks


class Deck:
    def __init__(self, deck_link, proxy):
        self.proxy = proxy
        """Selenium webdriver doesn't have async capabilities. Instantiating its webdriver as an async task"""
        self.driver = self.web_driver(proxy=self.proxy)
        self.deck_link = deck_link
        """ some ddb links are labeled as outdated but still considered competitive in the meta.
        This will make a valuable sortable datapoint"""
        self.link_group = self.sort_links()
        self.deck_hosted_on = self.sort_hosts()
        self.deck_data = self.get_deck_list()
        self.deck_list = self.deck_data[1]
        self.deck_name = self.deck_data[0]
        self.deck_author = self.deck_data[2]
        self.card_obj_list = []

    def disp_deck_data(self):
        print(f"Name: {self.deck_name}, Author: {self.deck_author}, List: {len(self.deck_list)}")
        return None

    def make_cards_obj(self, lst=None) -> list:
        if (len(self.deck_list) > 0) and (type(self.deck_list[-1]) is str):
            self.card_obj_list.append(Card(self.deck_list[-1]))
            self.deck_list.pop()
            self.make_cards_obj(self.deck_list)
        return self.deck_list

    def web_driver(self, proxy):
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('headless'),
        edge_options.add_argument('disable-gpu')
        edge_options.add_argument("--proxy_server=%s" % proxy)
        driver = selenium.webdriver.Edge(options=edge_options)
        return driver

    def sort_links(self) -> str:
        f = open('competitive_decks', 'r')
        file = f.read().strip().split('\n')
        if self.deck_link in file:
            self.link_group = "Competitive"
        else:
            self.link_group = "Outdated"
        f.close()
        return self.link_group

    def sort_hosts(self) -> str:
        # regex strips everything out of the given weblink to identify which deck website hosts the data.
        self.deck_hosted_on = re.sub(".+www\.|\.c.+|.n.+|^ht.+?//|\.o.+", '', self.deck_link)
        return self.deck_hosted_on

    def get_deck_list(self):
        match self.deck_hosted_on:
            case 'moxfield':
                return self.get_mx()
            case 'tappedout':
                return self.get_tppdout()

    def get_mx(self):
        deck_xpath = '/html/body/div[1]/main/div[8]/div[1]/div[2]/div[1]'
        author_xpath = "/html/body/div[1]/main/div[3]/div[2]/div[1]/div/div[1]/div/div[2]/div/span/a"
        name_xpath = "/html/body/div[1]/main/div[3]/div[2]/div[1]/div/form/h1/span/span"
        self.driver.get(self.deck_link)
        wait = WebDriverWait(self.driver, 30)
        deck_list = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.split('\n')
        deck_list = [
            re.sub(
                "^[0-9].+|^\d|^C.+\(.+\)|^A.+\(.+\)|^E.+\(.+\)|^B.+\(.+\)|^P.+\(.+\)|^I.+\(.+\)|^S.+\(.+\)|^L.+\(.+\)",
                '', card) for card in deck_list]
        self.deck_list = [name for name in deck_list if "1" not in name if "$" not in name if '' != name]
        author = wait.until(ec.presence_of_element_located((By.XPATH, author_xpath))).text.split('\n')
        self.deck_author = [auth for auth in author]
        self.deck_name = wait.until(ec.presence_of_element_located((By.XPATH, name_xpath))).text.strip()
        return self.deck_name, self.deck_list, self.deck_author

    def get_tppdout(self):
        name_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[1]/div/div/h2"
        author_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[1]/div/div/p[2]/a"
        deck_xpath = "/html/body/div[1]/div[1]/div[6]/div/div[1]/div[2]/div[2]/div[1]/div[2]"
        self.driver.get(self.deck_link)
        wait = WebDriverWait(self.driver, 30)
        self.deck_name = wait.until(ec.presence_of_element_located((By.XPATH, name_xpath))).text.strip()
        self.deck_author = wait.until(ec.presence_of_element_located((By.XPATH, author_xpath))).text.strip()
        self.deck_list = wait.until(ec.presence_of_element_located((By.XPATH, deck_xpath))).text.split("\n")
        self.deck_list = [
            re.sub(
                "^[0-9]*x\s|^\d|^C.+\(.+\)|^A.+\(.+\)|^E.+\(.+\)|^B.+\(.+\)|^P.+\(.+\)|^I.+\(.+\)|^S.+\(.+\)|^L.+\(.+\)",
            '', card) for card in self.deck_list]
        self.deck_list = [card.strip() for card in self.deck_list if '' != card]
        return self.deck_name, self.deck_list, self.deck_author


class Card(Deck):
    def __init__(self, card_name):
        super().__init__(self.deck_link, self.proxy)
        self.deck_link = self.deck_link
        self.proxy = self.proxy
        self.card_name = card_name
        self.card_dict = self.get_json_dict(card_name)
        self.card_layout = self.card_dict['layout']
        self.faces = self.make_faces(self.card_dict)
        self.legal_status = self.card_dict['legalities']['commander']

    def display_card(self):
        print(f"Card Name: {self.card_name}\n"
              f"Layout: {self.card_layout}")
        for face in self.faces:
            print(f"\ncmc: {face.cmc}, mc: {face.mana_cost}, type: {face.card_type}, colors: {face.color_ident}")

    def get_json_dict(self, card) -> Dict:
        link = "https://api.scryfall.com/cards/named?fuzzy=" + card
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        card_dict = json.loads(soup.text)
        time.sleep(.25)
        return card_dict

    async def req_json(self, session, api_link):
        VALID_STATUSES = [200, 301, 302, 307, 404]
        try:
            async with session.get(api_link, timeout=500) as resp:
                await resp.json()
                # asyncio.sleep is used to restrict requests to < 10 per sec, per skcryfall api guidelines.
                await asyncio.sleep(.12)
                if resp.status in VALID_STATUSES:
                    async with session.get(resp.url, timeout=500) as json_resp:
                        card_data = json.loads(await json_resp.read())
                        self.make_faces(card_data)
        except Exception as e:
            print(f"Exception: {e}")

    async def card_api(self):
        api_link = "https://api.scryfall.com/cards/named?fuzzy="
        tcp_connection = aiohttp.TCPConnector(limit=250)
        header = {"Authorization": "Basic bG9naW46cGFzcw=="}
        async with aiohttp.ClientSession(connector=tcp_connection, headers=header, trust_env=True) as session:
            try:
                tasks = [asyncio.create_task(self.req_json(session, api_link=api_link + card)) for card in self.deck_list]
                for task in tasks:
                    await task
            except Exception as e:
                print(f"Exception: {e}")
            await asyncio.sleep(0)


    def make_faces(self, card) -> list:
        faces = []
        try:
            for side in range(len(card['card_faces'])):
                faces.append(Face(face_name=card['card_faces'][side]['name'],
                                  cmc=card['cmc'], mana_cost=card['card_faces'][side]['mana_cost'],
                                  card_type=card['card_faces'][side]['type_line'],
                                  card_text=card['card_faces'][side]['oracle_text'],
                                  color_ident=card['color_identity']))
        except KeyError:
            faces.append(Face(face_name=card['name'], cmc=card['cmc'], mana_cost=card['mana_cost'],
                              card_type=card['type_line'], card_text=card['oracle_text'],
                              color_ident=card['color_identity']
                              ))
        return faces


@dataclass
class Face(Deck):
    face_name: str = field(default=str)
    cmc: float = field(default=float)
    mana_cost: str = field(default=str)
    card_type: str = field(default=str)
    card_text: List = field(default=list)
    color_ident: str = field(default=str)