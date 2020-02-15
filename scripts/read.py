#!/usr/bin/env python
from hepscrape import HepDataScraper
from storage import HepPub
hds = HepDataScraper()

# Print the ID and title for the first 25 publications
for i, pub in enumerate(hds.session().query(HepPub)):
    if i > 24:
        break
    print(pub.id, pub.title)