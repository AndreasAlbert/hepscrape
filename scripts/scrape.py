#!/bin/env python
from hepscrape import HepDataScraper

hds = HepDataScraper()

# Scrape the first three search pages for new entries
hds.find_pubs(max_pages=3)

# Find out more the entries
# Limit to 5 publications
hds.fill_pubs(max_pubs=5)