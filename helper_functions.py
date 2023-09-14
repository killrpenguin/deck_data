from selenium import webdriver
from selenium.webdriver import EdgeOptions
import selenium


def set_working(proxy, working_set):
    working_set.add(proxy)


def web_driver(*, proxy):
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument('headless'),
    edge_options.add_argument('disable-gpu')
    edge_options.add_argument("--proxy_server=%s" % proxy)
    driver = selenium.webdriver.Edge(options=edge_options)
    return driver

