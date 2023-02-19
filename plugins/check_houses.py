import asyncio
import os
from io import BytesIO

import requests
from aiogram.dispatcher import Dispatcher

from home_parser import MyHomeParser
from utils import log, shorten, warn
from .msg_txt_creator import get_msg_txt

first_time: bool  # признак того, что ссылка указана 1-й раз, и надо делать fetch


async def check_new_houses(dp: Dispatcher, sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        url = os.environ.get('URL')
        if not url:
            log.warning("# not url!")
            continue

        p = MyHomeParser(url)

        if p.status == 200:
            log.debug(f'status code: {p.status}')
        else:
            log.warning(f'Oh shit... We have a problem, status code: {p.status}')
            continue

        p.get_cards()
        p.get_homes_url_and_images()

        if not len(p.homes_url):
            warn("not len(p.homes_url)")
            continue

        p.save_to_env()

        if p.first_time:
            continue

        for i, url in enumerate(p.homes_url):
            # todo:
            msg = get_msg_txt(p, url, i)
            image_url = p.description['image_url'][i]

            # Download the image and sends it
            response = requests.get(image_url)
            user_ids = os.environ.get('USER_IDS', '').split(',')

            if not user_ids:
                log.error('<USER_IDS> is not founded or empty!')
                continue

            for user_id in user_ids:
                try:
                    log.info(f'# send_photo {user_id = }')
                    image_bytes_copy = BytesIO(response.content)
                    image_bytes_copy.seek(0)
                    await dp.bot.send_photo(user_id, photo=image_bytes_copy, caption=msg, parse_mode="Markdown")
                except Exception as e:
                    log.exception(f'Error while sending msg: {shorten(msg, 333)}')
