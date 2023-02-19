from typing import List

from aiogram.types import BotCommand
from aiogram.types.base import TelegramObject

from utils import logger, log_call, shorten
from utils import logging
from utils.telegrammy.err_handler import handle_cant_parse_entities_exception
from utils.telegrammy.telegram_bot import TelegramBot, send_message


def reg_bot_commands(res_commands: List[TelegramObject], **commands):
    for command, description in commands.items():
        res_commands.append(
            BotCommand(command=f'/{command}', description=description)
        )
        logging.debug(f"Added bot command {command}: {shorten(description, 1111)}")
    logging.debug(f"#2 {commands = }")
    return res_commands


TelegramBot, logger, log_call
