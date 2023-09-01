from ddb_list import ddb_objects
from card_object import Card

proxy = 'http://24.158.29.166:80'
target_objects = ddb_objects()
for target in target_objects:
    if 'moxfield' == target.link_group:
        target.get_mx(proxy=proxy)
        print(f'{target.deck_link} {target.deck_name} {target.category}, {target.deck_author}, {target.deck_commander}')
        for card in target.deck_list:
            card_obj = Card('', '', '', [], '')
            card_obj.populate_card_info(card, proxy)
            card_obj.print_card_details()
