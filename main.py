from scraper_targets import ddb_objects

f = open('ddb_obects', 'x')
target_objects = ddb_objects()
target_objects = [f.write(i.deck_link + '\n' +
                          i.category + '\n' +
                          i.link_group + '\n')
                  for i in target_objects]
f.close()
