# d from _log_call import _logd;_logd(__file__)
from typing import List

from aiogram.types import BotCommand
from aiogram.types.base import TelegramObject


def reg_bot_commands(res_commands: List[TelegramObject] = [], **commands):
    for command, description in commands.items():
        res_commands.append(
            BotCommand(command=f'/{command}', description=description)
        )
        # ? logging.debug(f"Added bot command {command}: {shorten(description, 1111)}")
    # logging.debug(f"#2 {commands = }")
    # logging.info(f"#2.1 {commands = }")
    return res_commands
