from scraper_targets import ddb_objects


proxy = 'http://45.225.184.177:999'
target_objects = ddb_objects()
for i in target_objects:
    if 'moxfield' == i.link_group:
        i.get_mx(proxy=proxy)
        print(f'{i.deck_link} {i.deck_name} {i.category} {len(i.deck_list)}')
