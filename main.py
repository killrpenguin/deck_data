from scraper_targets import ddb_objects
from card_object import Card

proxy = 'http://45.225.184.177:999'
target_objects = ddb_objects()
for target in target_objects:
    if 'moxfield' == target.link_group:
        target.get_mx(proxy=proxy)
        print(f'{target.deck_link} {target.deck_name} {target.category} {target.deck_list}, {target.deck_author}')
        for name in target.deck_list:
            print(name)
            card = Card(card_name=name, cmc='',
                        card_type='', legal_status='', card_text=[])
            card.populate_card_info(name, proxy=proxy)
            print(f'{card.card_name}, {card.cmc}, {card.card_type}, {card.legal_status}, {card.card_text}')
