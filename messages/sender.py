import os
from io import BytesIO
from typing import Union

import requests
from aiogram import types
from aiogram.dispatcher import Dispatcher

from home_parser import MyHomeParser
from messages.msg_txt_creator import get_msg_txt
from utils import log, shorten


async def send_messages(p: MyHomeParser, dp: Union[Dispatcher, types.Message]):
    this = send_messages.__name__
    try:
        # todo: consolidate with show_all()
        for i, url in enumerate(p.homes_url):
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
                    ##log.exception(f'Error while sending msg: {shorten(msg, 333)}')
                    log.error(f'## Error while sending msg:\n\n{msg}\n\n\n')
                    raise
    except:
        log.exception(f"## Global exception in {this}!")
        raise
