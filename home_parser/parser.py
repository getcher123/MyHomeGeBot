import logging
import os

import requests
from bs4 import BeautifulSoup

from settings.debug_settings import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)

class MyHomeParser:
    _headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36'}

    first_time:bool = False

    def __init__(self, url: str):
        self.request = requests.get(url=url, headers=self._headers)
        self.status = self.request.status_code
        self.soup = BeautifulSoup(self.request.text, 'lxml')
        self.cards = []
        self.homes_url = []
        self.description = {'image_url': [], 'title': [], 'price': [], 'square': [], 'stairs': [], 'address': []}
        self.old_url = os.environ.get('HOMES_URL', '').split(',')
        if(not self.old_url): 
            self.first_time = True;
            logging.debug("First time starting")

    def get_cards(self):
        all_cards = self.soup.select('div[class="statement-card"]')
        self.cards.extend(all_cards)

    def get_homes_url_and_images(self):
        for card in self.cards:
            card_href = card.find('a').get('href')[:37]
            if card_href not in self.old_url:
                logging.debug(f"Find unique url {card_href= }")

                self.homes_url.append(card_href)
                self.description['image_url'].append(card.find('img', class_='card-img')['data-src'])
                self.description['title'].append(card.find('h5', class_='card-title').text)
                self.description['price'].append(card.find('b', {'class': 'item-price-usd'}).text)
                self.description['square'].append(card.find('div', {'class': 'item-size'}).text)
                self.description['stairs'].append(card.select_one('.options-texts span').text)
                self.description['address'].append(card.find('div', class_='address').text)

    def save_to_env(self):
        logging.debug(f"Saving ... {self.homes_url= } {self.old_url= }")
        logging.debug(f"Extends ... {self.homes_url.extend(self.old_url) = }")

        if len(self.old_url):
            logging.debug("Old url is not empty")
            os.environ['HOMES_URL'] = ','.join(self.homes_url.extend(self.old_url))
        else:
            os.environ['HOMES_URL'] = ','.join(self.homes_url)

    def __del__(self):
        self.request.close()
        del self