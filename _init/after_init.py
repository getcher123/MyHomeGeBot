import asyncio
import logging

from aiogram import Bot
from loguru import logger as log

from bot.bot_commands_settings import commands
from plugins import check_new_houses
# from settings import conf
from settings.webhook_settings import WEBHOOK_URL


async def on_startup(
        dispatcher
) -> None:
    assert dispatcher
    from tg_bot import dp, bot
    assert all((bot, dp)), (bot, dp)

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await bot.set_my_commands(commands)

    loop = asyncio.get_event_loop()
    from _init import globals as conf
    loop.create_task(check_new_houses(dp, sleep_time=conf.TIMEOUT))


async def on_shutdown(
        dispatcher
) -> None:
    from tg_bot import bot
    assert bot
    await bot.delete_webhook()


def set_commands(bot: Bot):
    log.info("# Registration of commands displayed in the Telegram interface:..")
    assert commands
    logging.debug(f'#3 {commands = }')
