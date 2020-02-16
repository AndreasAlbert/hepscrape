from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = 'hepscrape',
    version = '0.0.1',
    url = 'https://github.com/AndreasAlbert/hepscrape',
    author = 'Andreas Albert',
    author_email = 'andreas.albert@cern.ch',
    description = 'Simple web scraper for hepdata meta data',
    packages = find_packages(),    
    install_requires = requirements,
)
