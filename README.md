# HepScrape
HepScrape is a simple tool to scrape the meta data of all entries on [hepdata](www.hepdata.net).
The meta data is stored in an sqlite data base.


## Working principle

The scraping happens in two steps:

1. Finding publications: The hepdata search pages are sequentially pulled and a unique entry ID, as well as the entry title are stored. This step is relatively fast because there are many entries per search page index.

2. Filling the rest of the information: For each publication we have found in the first step, the individual entry page is pulled and parsed for more detailed information, which is then stored.

In both cases, an effort is made to avoi duplicate work. Only entries that are not yet present are updated in step 1, and only entries that do not have all information stored are updated in step 2.


## How to scrape
Usage is straightforward, and a one-click solution can be found in `scripts/scrape.py`, which looks like this:

```python
from hepscrape import HepDataScraper

hds = HepDataScraper()

# Scrape the first three search pages for new entries
hds.find_pubs(max_pages=3)

# Find out more the entries
# Limit to 5 publications
hds.fill_pubs(max_pubs=5)
```

## How to read
The information is stored in sqlite format using the `sqlalchemy` python library and can be read back with standard syntax.
An example can be found in `scripts/read.py`:


```python
from hepscrape import HepDataScraper
from storage import HepPub
hds = HepDataScraper()

# Print the ID and title for the first 25 publications
for i, pub in enumerate(hds.session().query(HepPub)):
    if i > 24:
        break
    print(pub.id, pub.title)
```