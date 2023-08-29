from scraper_targets import ddb_objects
from card_object import Card

proxy = 'http://45.225.184.177:999'
target_objects = ddb_objects()
for i in target_objects:
    if 'moxfield' == i.link_group:
        i.get_mx(proxy=proxy)
        print(f'{i.deck_link} {i.deck_name} {i.category} {i.deck_list}, {i.deck_author}')
        for name in i.deck_list:
            print(name)
            card = Card(card_name=name, cmc='',
                        card_type='', legal_status='', card_text=[])
            card.populate_card_info(name, proxy=proxy)
            print(f'{card.card_name}, {card.cmc}, {card.card_type}, {card.legal_status}, {card.card_text}')
