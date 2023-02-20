import re
from typing import Tuple, Optional

import aiogram.utils
import aiogram.utils.exceptions

import tg_bot


class TelegramError(Exception): pass


class TelegramErrorHandler:
    @staticmethod
    def fix_caption_text(caption_text: str) -> str:
        """
        Check for unclosed tags or mismatched brackets and fix them
        Alternatively, remove all formatting from the caption text
        Return the fixed caption text

        >>> TelegramErrorHandler.fix_caption_text('<b>test</i>')
        '<b>test</b>'

        >>> TelegramErrorHandler.fix_caption_text('<b>test</b>')
        '<b>test</b>'

        >>> TelegramErrorHandler.fix_caption_text('<b>test')
        '<b>test</b>'

        >>> TelegramErrorHandler.fix_caption_text('test')
        'test'
        """
        open_tags = re.findall(r'<[^/].*?>', caption_text)
        close_tags = re.findall(r'</.*?>', caption_text)
        open_tags.reverse()

        for open_tag in open_tags:
            close_tag = '</' + open_tag[1:]
            if close_tag not in close_tags:
                caption_text += close_tag
                close_tags.append(close_tag)

        for close_tag in close_tags:
            open_tag = '<' + close_tag[2:]
            if open_tag not in open_tags:
                caption_text = open_tag + caption_text
                open_tags.append(open_tag)

        return re.sub(r'<.*?>', '', caption_text)

    @classmethod
    async def handle_cant_parse_entities_exception(cls, update, fix_caption_text=True) -> Tuple[
        str, Optional[Exception]]:
        try:
            if fix_caption_text:
                caption_text = cls.fix_caption_text(update.message.caption)
            else:
                caption_text = update.message.caption
            await tg_bot.bot.send_photo(chat_id=update.effective_chat.id, photo=update.message.photo[-1].file_id,
                                        caption=caption_text)
        except aiogram.utils.exceptions.CantParseEntities as e:
            reason, _ = cls.determine_error_reason(str(e), e)
            ##? await context.bot.send_message(chat_id=update.effective_chat.id, text=reason)
            from utils.telegrammy import send_message

            await send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {reason}")
            return reason, e

    @staticmethod
    def determine_error_reason(error_message: str, exception=None) -> Tuple[str, Optional[Exception]]:
        if "Can't parse entities" in error_message:
            start_index = error_message.find('starting at byte offset ') + len('starting at byte offset ')
            end_index = error_message.find('.', start_index)
            byte_offset = int(error_message[start_index:end_index])
            bad_symbols = error_message[byte_offset:]
            reason = f"There is a problem with parsing the entities in the caption text of the photo message. The error is happening when trying to parse the entities starting at byte offset {byte_offset}. The bad symbols are: {bad_symbols}."
            return reason, exception
        else:
            return "Unknown error", exception



def determine_error_reason(error_message: str, exception: Optional[Exception] = None) -> Tuple[str, Optional[Exception]]:
    """
    Determines the reason for an error message related to parsing entities in a caption text of a photo message.

    Args:
        error_message (str): The error message to analyze.
        exception (Optional[Exception]): The exception object associated with the error message. Defaults to None.

    Returns:
        Tuple[str, Optional[Exception]]: A tuple containing the reason for the error message and the exception object, if any.

    Example:
        >>> determine_error_reason("Can't parse entities: can't find end of the entity starting at byte offset 59.")
        ("There is a problem with parsing the entities in the caption text of the photo message. The error is happening when trying to parse the entities starting at byte offset 59. The bad symbols are: .", None)

    """
    if "Can't parse entities" in error_message:
        start_index = error_message.find('starting at byte offset ') + len('starting at byte offset ')
        end_index = error_message.find('.', start_index)
        byte_offset = int(error_message[start_index:end_index])
        bad_symbols = error_message[byte_offset:]
        return f"There is a problem with parsing the entities in the caption text of the photo message. The error is happening when trying to parse the entities starting at byte offset {byte_offset}. The bad symbols are: {bad_symbols}.", exception
    else:
        return "Unknown error", exception


handle_cant_parse_entities_exception = TelegramErrorHandler.handle_cant_parse_entities_exception
# ~?^
# def handle_cant_parse_entities_exception(func):
#     @wraps(func)
#     async def wrapper(update, context, *args, **kwargs):
#         try:
#             return await func(update, context, *args, **kwargs)
#         except aiogram.utils.exceptions.CantParseEntities as e:
#             error_msg = str(e)
#             error_reason, _ = determine_error_reason(error_msg, e)
#             ##await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {error_reason}")
#             await send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {error_reason}")
#     return wrapper
