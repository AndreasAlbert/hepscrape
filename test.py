#!/bin/env python
import requests
from bs4 import BeautifulSoup

# url = 'https://www.hepdata.net/record/ins1517194'
# page = requests.get(url)
# with open("dump.html","w") as f:
#     f.write(page.text)

# print(page.text)

# with open("dump.html","r") as f:
#     soup = BeautifulSoup(f.read(), "html.parser")


# publications = soup.find_all(id=lambda x: x.startswith("publication-") if x else False)

# for pub in publications:
#     # print(pub)
#     # break
#     header = pub.find('h4',class_="record-header")

#     publication_collaboration = pub.find('span',class_="info_group").text.strip()

#     link = header.find('a')
#     publication_title = link.text.strip()
#     publication_identifier = link['href']

#     print(publication_identifier, publication_collaboration, publication_title)
#     print(header.content)
# for result in results:
#     print("---------")
#     print(result)

# journal = soup.find('div',class_='record-journal').text.strip()
# year = journal.split(',')[-1]
# inspire_id = soup.find('a',href=lambda x: 'inspirehep' in x)['href'].split('/')[-1]


from hepdata import HepDataScraper
from storage import HepPub
hds = HepDataScraper()
# hds.scrape()

pub = hds._session.query(HepPub).first()