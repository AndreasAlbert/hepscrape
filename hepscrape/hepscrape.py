import logging as log
import os

import requests

from bs4 import BeautifulSoup
from hepscrape.storage import Base, HepPub
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

log.basicConfig(level=log.INFO)

class HepDataScraper(object):
    search_url = 'https://www.hepdata.net/search/?q='

    def __init__(self, dbpath = "hepdata.db"):
        """Initialization

        The main initialization task is to set up
        the sqlalchemy session. If the data base
        does not exist yet, a new one is created.
        
        :param dbpath: Path to the data base file, defaults to "hepdata.db"
        :type dbpath: str, optional
        """
        
        # Check if we need to create a new DB
        new = not os.path.exists(dbpath)
        
        # Make sure the folder exists
        if new:
            dbdir = os.path.abspath(os.path.dirname(dbpath))
            try:
                os.makedirs(dbdir)
            except FileExistsError:
                pass

        # Start the engine and create structure if needed
        engine =  create_engine(f'sqlite:///{dbpath}')
        if new:
            Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def _parse_publication_block(self,block):
        """
        Creates a HepPub object from an HTML representation.

        :param block: The HTML representation of a publication 
                      from the hepdata search page
        :type block: 
        :return: A publication object representing the block
        :rtype: HepPub
        """
        header = block.find('h4',class_="record-header")

        hp = HepPub()
        link = header.findChild('a',recursive=False)

        hp.title = link.text.strip()
        hp.id = link['href']

        try:
            hp.collaboration = block.find('span',class_="info_group").text.strip()
        except AttributeError:
            hp.collaboration = None

        return hp

    def _scrape_search_page(self,index):
        """
        Scrapes the search page with a given page index
        
        :param index: Page index of search page to scrape.
        :type index: int
        """
        log.debug(f'Scraping page index {index}.')
        
        # Retrieve the corresponding page from the web
        page = requests.get(f"{self.search_url}&page={index}&size=100")

        # If we ask for an index that is too high,
        # we will get an internal server error 500
        # which is our cue to stop
        if not page.ok:
            return False

        # Parse the page we got
        soup = BeautifulSoup(page.content, "html.parser")
        publications = soup.find_all(id=lambda x: x.startswith("publication-") if x else False)

        # Add entries that do not exist yet
        for hp in map(self._parse_publication_block, publications):
            exists = self._session.query(HepPub.id).filter_by(id=hp.id).scalar() is not None
            if exists:
                continue
            self._session.add(hp)
        
        self._session.commit()

        return True

    def _update_publication(self, pub):
        """
        Updates a publication to the current status on the web
        
        The publication object is modified in-place!

        :param pub: The publication object to update
        :type pub: HepPub
        :raises RuntimeError: If the page can not be loaded.
        """
        url = f'https://www.hepdata.net/{pub.id}'

        page = requests.get(url)

        if not page.ok:
            raise RuntimeError()

        soup = BeautifulSoup(page.content, "html.parser")

        pub.journal = soup.find('div',class_='record-journal').text.strip()
        pub.year = pub.journal.split(',')[-1]
        pub.inspire = soup.find('a',href=lambda x: 'inspirehep' in x)['href'].split('/')[-1]


    def find_pubs(self, max_pages=0):
        """
        Find out which publications exist.
        
        First step of the scraping process:
        Sequentially pulls search pages. 
        For new publications, bare bones 
        info is stored in the data base.
        """
        log.info("Searching for new publications.")
        if max_pages:
            log.info(f"Will pull information from a maximum of {max_pages} search pages.")
        else:
            log.info("Will pull information from an unlimited number of search pages.")

        i = 1
        good = True
        while good:
            if max_pages and (i>=max_pages):
                break
            good = self._scrape_search_page(i)
            i+=1
        log.info("Finished searching.")

    def fill_pubs(self, max_pubs=0):
        """
        Flesh out the per-publication information

        Second step of the process: For publications
        lacking at least one field, pull their individual
        pages, and parse + store info in data base.
        """
        log.info("Filling publication information.")
        if max_pubs:
            log.info(f"Will pull information for a maximum of {max_pubs} publications.")
        else:
            log.info("Will pull information for an unlimited number of publications")

        pulls = 0
        for pub in self._session.query(HepPub):
            if max_pubs and pulls >= max_pubs:
                break
            if pub.is_complete():
                continue
            self._update_publication(pub)
            self._session.commit()
            pulls+=1
        log.info(f"Finished updating publications.")
    def session(self):
        """[summary]
        
        :return: [description]
        :rtype: [type]
        """
        return self._session
