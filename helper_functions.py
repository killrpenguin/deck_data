from selenium import webdriver
from selenium.webdriver import EdgeOptions
import selenium


def set_working(proxy, working_set):
    working_set.add(proxy)



def web_driver(*, proxy, deck_address, pause):
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'), edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    driver.get(deck_address)
    driver.implicitly_wait(pause)
    return driver