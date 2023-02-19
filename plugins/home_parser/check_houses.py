from aiogram.dispatcher import Dispatcher

from plugins.home_parser import MyHomeParser
from messages.sender import send_messages
from utils import warn
from utils.common import sleep, get_var

first_time: bool  # признак того, что ссылка указана 1-й раз, и надо делать fetch


async def check_new_houses(dp: Dispatcher, sleep_time: int):
    while True:
        await sleep(sleep_time)

        if not (url := get_var('URL')): continue

        p = MyHomeParser(url)
        # ?r if not check_status(p): continue
        if not p.check_status(): continue
        p.get_cards()
        p.get_homes_url_and_images()

        if not len(p.homes_url):
            warn("not len(p.homes_url)")
            continue

        p.save_to_env()

        if p.first_time: continue

        await send_messages(p, dp)
