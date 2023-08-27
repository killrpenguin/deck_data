from scraper_targets import ddb_objects
from deck_objects import Deck
import helper_functions


proxy = "http://103.77.60.14:80"
driver = helper_functions.web_driver(proxy=proxy)
target_objects = ddb_objects()
decks = []
for i in target_objects:
    print(f'{i.deck_link}')
    if 'moxfield' == i.link_group:
        mx_deck = Deck(deck_link=i.deck_link, link_group=i.link_group,
                    category=i.category, driver=driver)
        decks.append(mx_deck)
        driver.close()
        print(decks)
