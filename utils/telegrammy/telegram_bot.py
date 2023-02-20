import re

from aiogram import Bot
from fastcore.foundation import L

from utils import logger, log_call
from utils.telegrammy.err_handler import TelegramError
from utils.telegrammy.err_handler import handle_cant_parse_entities_exception


# from main import telegramBot
# send_message = telegramBot.send_message


class TelegramBot:
    MAX_MESSAGE_LENGTH = 200

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot = Bot(token=bot_token)
        self.send_message_handled = handle_cant_parse_entities_exception(TelegramBot.send_message)
        self.send_photo_handled = handle_cant_parse_entities_exception(TelegramBot.send_photo)

    @staticmethod
    def is_message_correct(text: str) -> (bool, str):
        """
        Checks if a given message is correct and returns a tuple of a boolean value indicating if the message is correct
        and a string containing any detailed information about the incorrect symbols.

        :param text: The text to check.
        :return: A tuple of a boolean value and a string.

        >>> TelegramBot.is_message_correct("Hello, world!")
        (True, '')
        >>> TelegramBot.is_message_correct("This message is too long to be sent to Telegram.")
        (False, 'The message is too long. ')
        >>> TelegramBot.is_message_correct("This message contains $pecial characters.")
        (False, 'The message contains special characters: $')
        """
        is_correct = True
        incorrect_symbols = ""

        # Check the length of the text
        if len(text) > TelegramBot.MAX_MESSAGE_LENGTH:
            is_correct = False
            incorrect_symbols += "The message is too long. "

        # Check for any special characters in the text
        special_chars = L(re.findall('[^a-zA-Z0-9_ ]', text))
        if special_chars:
            is_correct = False
            incorrect_symbols += f"The message contains special characters: {special_chars.uniq()}"

        return is_correct, incorrect_symbols

    # @staticmethod
    # @log_call
    # # /Users/user/github.com/getcher123/MyHomeGeBot/utils/telegrammy/telegram_bot.py
    # def make_message_correct(text: str) -> str:
    #     """
    #     Makes a given message correct by removing any special characters and shortening it if necessary.
    #
    #     :param text: The text to make correct.
    #     :return: The corrected text.
    #
    #     >>> TelegramBot.make_message_correct("This message contains $pecial characters and is too long to be sent to Telegram.")
    #     'This message contains pecial characters and is too long to be sent to Telegram'
    #     >>> TelegramBot.make_message_correct("This message is too long to be sent to Telegram.")
    #     'This message is too long to be sent to Telegram'
    #     """
    #     # Remove any special characters
    #     corrected_text = re.sub('[^a-zA-Z0-9_ ]', '', text)
    #
    #     # Shorten the message if necessary
    #     if len(corrected_text) > TelegramBot.MAX_MESSAGE_LENGTH:
    #         corrected_text = corrected_text[:TelegramBot.MAX_MESSAGE_LENGTH]
    #
    #     return corrected_text

    ##@handle_cant_parse_entities_exception
    async def send_message(self, chat_id: int, text: str, auto_correct: bool = False) -> None:
        """
        Sends a message to a Telegram chat using the specified bot token and chat ID, with optional auto-correction or
        error raising.

        :param chat_id: The chat ID to send the message to.
        :param text: The text to send.
        :param auto_correct: Whether to auto-correct the message or raise an error if the message is incorrect.
        :raises ValueError: If the message is incorrect and auto-correction is disabled.
        :raises TelegramError: If there is an error sending the message.
        :return: None
        >>> bot = TelegramBot("BOT_TOKEN")
        >>> bot.send_message(123456789, "Hello, world!")
        >>> bot.send_message(123456789, "This message is too long to be sent to Telegram.")
        Traceback (most recent call last):
        ...
        ValueError: The message is incorrect: The message is too long.
        >>> bot.send_message(123456789, "This message contains $pecial characters.")
        Traceback (most recent call last):
        ...
        ValueError: The message is incorrect: The message contains special characters: $"

        # Example with auto-correction enabled
        >>> bot.send_message(123456789, "This message contains $pecial characters.", auto_correct=True)
        >>> bot.send_message(123456789, "This message is too long to be sent to Telegram.", auto_correct=True)
        >>> bot.send_message(123456789, "This message contains $pecial characters and is too long to be sent to Telegram.", auto_correct=True)

        # Example with loguru
        >>> bot.logs = logs
        >>> bot.send_message(123456789, "This message contains $pecial characters.")
        WARNING:telegram_bot:The message is incorrect: The message contains special characters: $"
        """

        # Check if the message is correct

        is_correct, incorrect_symbols = self.is_message_correct(text)
        if not is_correct:
            if auto_correct:
                # Auto-correct the message
                text = self.make_message_correct(text)
            else:
                # Raise an error
                raise ValueError(f"The message is incorrect: {incorrect_symbols}")

        try:
            # Send the message
            self.bot.send_message(chat_id=chat_id, text=text)
        except TelegramError as e:
            logger.exception(f"Error sending message to chat {chat_id}: {e}")
            raise e

    @log_call
    # @handle_cant_parse_entities_exception
    async def send_photo(self, chat_id: int, photo_url: str, caption: str = None,
                         auto_correct: bool = False, **send_photo_kwargs
                         ) -> None:
        """
        Sends a photo to a Telegram chat using the specified bot token and chat ID, with optional auto-correction or
        error raising.

        :param chat_id: The chat ID to send the photo to.
        :param photo_url: The URL of the photo to send.
        :param caption: The caption to add to the photo.
        :param auto_correct: Whether to auto-correct the caption or raise an error if the caption is incorrect.
        :raises ValueError: If the caption is incorrect and auto-correction is disabled.
        :raises TelegramError: If there is an error sending the photo.
        :return: None

        >>> bot = TelegramBot("BOT_TOKEN")
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This is a caption.")
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This caption is too long to be sent to Telegram.")
        Traceback (most recent call last):
        ...
        ValueError: The caption is incorrect: The message is too long.
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This caption contains $pecial characters.")
        Traceback (most recent call last):
        ...
        ValueError: The caption is incorrect: The message contains special characters: $"

        # Example with auto-correction enabled
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This caption contains $pecial characters.", auto_correct=True)
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This caption is too long to be sent to Telegram.", auto_correct=True)

        # Example with loguru

    Николай Крупий
    continue from part:
        # Example with loguru

    python

        >>> bot.logs = logs
        >>> bot.send_photo(123456789, "https://example.com/photo.jpg", "This caption contains $pecial characters.")
        WARNING:telegram_bot:The caption is incorrect: The message contains special characters: $"
        """

        # Check if the caption is correct
        is_correct, incorrect_symbols = self.is_message_correct(caption)
        if not is_correct:
            if auto_correct:
                # Auto-correct the caption
                caption = self.make_message_correct(caption)
            else:
                # Raise an error
                raise ValueError(f"The caption is incorrect: {incorrect_symbols}")

        try:
            # Send the photo
            await self.bot.send_photo(chat_id=chat_id, photo=photo_url, caption=caption, **send_photo_kwargs)
        except TelegramError as e:
            logger.exception(f"Error sending photo to chat {chat_id}: {e}")
            raise e

