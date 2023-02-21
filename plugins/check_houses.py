import asyncio
import logging
import os
from io import BytesIO

import requests
from aiogram.dispatcher import Dispatcher

from home_parser import MyHomeParser

first_time: bool


async def check_new_houses(dp: Dispatcher, sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        url = os.environ.get('URL')
        if not url:
            logging.warning("# not url!")
            continue

        p = MyHomeParser(url)

        if p.status == 200:
            logging.debug(f'status code: {p.status}')
        else:
            logging.warning(
                f'Oh shit... We have a problem, status code: {p.status}')
            continue

        p.get_cards()
        p.get_homes_url_and_images()

        if not len(p.homes_url):
            continue

        p.save_to_env()

        if p.first_time:
            continue

        for i, url in enumerate(p.homes_url):
            msg = f"**[{p.description['title'][i]}]({url})** - \n*${p.description['price'][i]}*     {p.description['square'][i]}     {p.description['stairs'][i]} \n{p.description['address'][i]}"
            image_url = p.description['image_url'][i]

            # Download the image and sends it
            response = requests.get(image_url)
            user_ids = os.environ.get('USER_IDS', '').split(',')
            if not user_ids:
                logging.error('Users ID is not founded')
                continue

            for user_id in user_ids:
                try:
                    logging.info(f'# send_photo {user_id = }')
                    image_bytes_copy = BytesIO(response.content)
                    image_bytes_copy.seek(0)
                    await dp.bot.send_photo(user_id, photo=image_bytes_copy, caption=msg, parse_mode="Markdown")
                except Exception as e:
                    logging.exception('Sending msg error')
