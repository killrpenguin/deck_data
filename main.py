from ddb_list import ddb_objects
from card_object import Card

proxy = 'http://24.158.29.166:80'
target_objects = ddb_objects()
for target in target_objects:
    if 'moxfield' == target.link_group:
        target.get_mx(proxy=proxy)
        print(f'{target.deck_link} {target.deck_name} {target.category}, {target.deck_author}, {target.deck_commander}')
        for card_obj in target.deck_list:
            card_name = target.deck_list.pop()
            target.deck_list.append(Card(card_name=card_name))
        for i in target.deck_list:
            print(i.face_name)