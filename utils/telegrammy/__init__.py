# from main import telegramBot
from _init.conf import TOKEN
from settings.conf import CONF
from utils import logger, log_call
from utils.telegrammy.err_handler import handle_cant_parse_entities_exception
from utils.telegrammy.telegram_bot import TelegramBot

if CONF.INIT_TelegramBot:
    telegramBot = TelegramBot(TOKEN)

##send_photo = telegramBot.send_photo_handled
# send_message = telegramBot.send_message_handled

@log_call
async def send_photo(*a, **k):
    await telegramBot.send_photo_handled(
        *a,
        parse_mode="Markdown",
        auto_correct=CONF.AUTO_CORRECT,
        **k)


@log_call
async def send_message(*a, **k):
    await telegramBot.send_message_handled(
        *a,
        # parse_mode="Markdown",
        auto_correct=CONF.AUTO_CORRECT,
        **k)


(
    # TelegramBot,
    logger, log_call
)
