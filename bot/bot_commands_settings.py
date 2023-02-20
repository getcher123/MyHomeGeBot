"""Configuring commands displayed in the Telegram interface"""

from bot.tools import reg_bot_commands

# commands = [
#     BotCommand(command="/start", description="Bot start🚀"),
#     BotCommand(command="/help", description="Help🆘"),
#     BotCommand(command='/set_link', description='установить новую ссылку для поиска'),
#     BotCommand(command='/show', description='посмотреть всю выдачу'),
#     BotCommand(command='/cancel', description='отменить действие'),
#     BotCommand(command='/show_link', description='Посмотреть текущую ссылку для поиска')
# ]
# logging.debug(f"#1 {commands = }")
# # # odo: use this:
# # commands_dict = dict(
# #     start="Bot start🚀",
# # )

# test:π
commands = reg_bot_commands(
    start="Bot start🚀",
    help="Help🆘",
    set_link='установить новую ссылку для поиска',
    show='посмотреть всю выдачу',
    cancel='отменить действие',
    show_link='Посмотреть текущую ссылку для поиска',
)
