"""Configuring commands displayed in the Telegram interface"""
# import logging
# from typing import List

from aiogram.types import BotCommand
# from aiogram.types.base import TelegramObject
# from utils import shorten

# List of commands
commands = [
    BotCommand(command="/start", description="Bot start🚀"),
    BotCommand(command="/help", description="Help🆘"),
    BotCommand(command='/set_link', description='установить новую ссылку для поиска'),
    BotCommand(command='/show', description='посмотреть всю выдачу'),
    BotCommand(command='/cancel', description='отменить действие'),
    BotCommand(command='/show_link', description='Посмотреть текущую ссылку для поиска')
]

# #todo: use this:
# commands_dict = dict(
#     start="Bot start🚀",
# )

# #todo: or better this:
# def reg_bot_commands(res_commands: List[TelegramObject], **commands):
#     for command, description in commands.items():
#         res_commands.append(
#             BotCommand(command=description)
#         )
#         logging.debug(f"Added bot command {}: {shorten(description, 1111)}")
#     return res_commands
#
# commands = reg_bot_commands(
#     start="Bot start🚀",
#     help="Help🆘",
#     set_link='установить новую ссылку для поиска',
#     show='посмотреть всю выдачу',
#     cancel='отменить действие',
#     show_link='Посмотреть текущую ссылку для поиска',
# )