from main import telegramBot
from settings.conf import CONF
from utils import logger, log_call
from utils.telegrammy.err_handler import handle_cant_parse_entities_exception
from utils.telegrammy.telegram_bot import TelegramBot, send_message

TelegramBot, logger, log_call

if CONF.INIT_TelegramBot:
    telegramBot = TelegramBot(TOKEN)

send_message = telegramBot.send_message_handled