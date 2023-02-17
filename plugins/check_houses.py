import asyncio

from messages import MESSAGES
from home_parser import MyHomeParser
from aiogram.dispatcher import Dispatcher
import os
import logging

logging.basicConfig(level=logging.INFO)

from io import BytesIO
import requests

logging.basicConfig(level=logging.INFO)

async def check_new_houses(dp:Dispatcher, sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        url = os.environ.get('URL')
        if not url:
            continue
        p = MyHomeParser(url)
        if p.status == 200:
            print(f'status code: {p.status}')
        else:
            print(f'Oh shit... We have a problem, status code: {p.status}')
            continue
        p.get_cards()
        p.get_homes_url_and_images()
        if len(p.homes_url):
            p.save_to_env()
        else:
            continue
        for i, url in enumerate(p.homes_url):
            msg = f"**[{p.description['title'][i]}]({url})** - ${p.description['price'][i]} {p.description['square'][i]}m²"
           
            
            
            image_url = p.description['image_url'][i]
            # Download the image and sendz it
            response = requests.get(image_url)
            image_bytes = BytesIO(response.content)
            user_ids = os.environ.get('USER_IDS', '').split(',')
            logging.info(f'{user_ids = }')
            for user_id in user_ids:
                try:
                    logging.info(f'{user_id = }')
                    await dp.bot.send_photo(user_id, photo=image_bytes, caption=msg, parse_mode="Markdown")
                except Exception as e:
                    print(e)
                

