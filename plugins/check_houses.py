from aiogram.dispatcher import Dispatcher

from home_parser import MyHomeParser
from home_parser.parser import check_status
from messages.sender import send_messages
from utils import warn, get_var
from utils.common import sleep

first_time: bool  # признак того, что ссылка указана 1-й раз, и надо делать fetch


async def check_new_houses(dp: Dispatcher, sleep_time: int):
    while True:
        await sleep(sleep_time)

        if not (url := get_var('URL')): continue

        p = MyHomeParser(url)

        if not check_status(p): continue

        p.get_cards()
        p.get_homes_url_and_images()

        if not len(p.homes_url):
            warn("not len(p.homes_url)")
            continue

        p.save_to_env()

        if p.first_time: continue

        await send_messages(p, dp)
