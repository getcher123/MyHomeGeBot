import asyncio

from bot.bot_commands_settings import commands
from plugins import check_new_houses
from settings.webhook_settings import WEBHOOK_URL
from . import conf


async def on_startup(
        dispatcher
) -> None:
    assert dispatcher
    from main import bot, dp
    assert all((bot, dp))

    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await bot.set_my_commands(commands)

    loop = asyncio.get_event_loop()
    loop.create_task(check_new_houses(dp, conf.TIMEOUT))


async def on_shutdown(
        dispatcher
) -> None:
    from main import bot
    assert bot
    await bot.delete_webhook()

