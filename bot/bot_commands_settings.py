"""Configuring commands displayed in the Telegram interface"""

from bot.tools import reg_bot_commands

commands = reg_bot_commands(
    start="Bot start🚀",
    help="Help🆘",
    set_link='установить новую ссылку для поиска',
    show='посмотреть всю выдачу',
    cancel='отменить действие',
    show_link='Посмотреть текущую ссылку для поиска',
)
