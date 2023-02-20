#todo:
# 4cg:
# improve this code, add typing, doctests, wrap into class, if it'll be better design:
# use reST-styled docstrings and make them maximally shorter, use fastcore.store_attrs(), use @dataclass, if it's suiteable, improve var-names where it's suitable
import re
from typing import Dict, Tuple

from plugins.home_parser import MyHomeParser
from utils import log, log_call

# from utils.telegrammy import TelegramBot

Url = str


def if_exc_ret_err_txt(f):
    def w(*a, **k):
        try:
            return f(*a, **k)
        except Exception as e:
            # return str(e)
            log.error(str(e))
            return f"Some error in {f.__name__}({a if a else ''}, {k if k else ''})"

    return w


@if_exc_ret_err_txt
@log_call
def get_tags_txt(full_desc_info: str, *, address: str = '', price: str = ''):
    address = address or full_desc_info.splitlines()[1]
    tags = []

    tags += address.split(' ')[-1]

    price_val = get_price_val(price)
    if price_val: tags += [get_tags_4_price(price_val)]

    tags = list(map(lambda a: f"#{a}", tags))
    log.debug(f"# {tags = }")
    tags_txt = ' '.join(tags)
    return tags_txt


@log_call
def convert_int(var, val) -> int:
    try:
        price_val = int(val)
    except:  # fixme ?n
        log.exception(f"Error <{var}> convert! {val = }")
    else:
        return price_val


def get_price_val(price) -> int:
    return convert_int('price',
                       price
                       .replace('м2', '')
                       .replace(' ', '')
                       )


@if_exc_ret_err_txt
@log_call
def get_price_2_sqr_val(price, square):
    price_val = get_price_val(price)
    square_val = convert_int('square', square.replace(' м²', '')
                             )
    # price_2_sqr_val = '<unknown>' if not all((price_val, price_val)) else square_val / price_val
    if not all((price_val, price_val)):
        price_2_sqr_val = '<unknown>'
    else:
        price_2_sqr_val = square_val / price_val
    return price_2_sqr_val


@if_exc_ret_err_txt
@log_call
def get_tags_4_price(price_val: int, *, max_=1000):
    """
    >>> for p in (11, 150, 300, 900, 1111): print(p, get_tags_4_price(p))
    11 0_100
    150 100_200
    300 300_400
    900 900
    1111 900+
    """
    prices_diaps: Dict[str: Tuple[int, int]] = {}
    prev = 0
    for price in range(0, max_, 100):
        # _logd(f"{(prev, price) = }")
        prices_diaps.update({
            f"{prev}_{price}": (prev, price)
        })
        prev = price
    for name, (from_, to_) in prices_diaps.items():
        if from_ <= price_val < to_:
            return f"{name}"
        max_ = to_
    if price_val == max_:
        return f"{max_}"
    if price_val >= max_:
        return f"{max_}+"
    else:
        return "undefined_price_interval!"


@log_call
def get_msg_txt(p: MyHomeParser, url: Url, i: int, *,
                prop_sep='     ',
                ):
    title = p.description['title'][i]
    price = p.description['price'][i]
    square = p.description['square'][i]
    stairs = p.description['stairs'][i]
    address = p.description['address'][i]

    title = title

    price = price
    square = square.replace('.00', '')
    stairs = stairs.replace('Этаж', 'эт.')
    address = (address
               .replace(', Батуми', '')
               .replace(', Аджара', '')
               )
    if title == 'Сдается в аренду новопостроенная квартира':
        address, title = '', address

    # i msg = f"**[{p.description['title'][i]}]({var_val})** - \n*${p.description['price'][i]}*     {p.description['square'][i]}     {p.description['stairs'][i]} \n{p.description['address'][i]}"
    full_descr_info = (f"**[{title}]({url})** -"
                       f" \n"
                       f"*${price}*"
                       f"{prop_sep}{square}"
                       f"{prop_sep}{stairs}"
                       f" \n"
                       f"{address}")

    try:
        tags_txt = get_tags_txt(full_descr_info, price=price, address=address)
        price2square_info = get_price_2_sqr_val(price, square)
        add_info = (
            f"\n"
            #e1 f"price-to-square: {price2square_info}"
            f"\n"
            f"{tags_txt}"
        )
    except Exception as e:
        log.exception(f"Fatal exception in {get_msg_txt.__name__}")
        add_info = str(e)

    return check_text_4_bot(f"{full_descr_info}"
                            f" \n"
                            f"{add_info}"
                            )


def check_text_4_bot(text: str) -> str:
    # text = TelegramBot.make_message_correct(text)
    text = make_message_correct(text)
    return text


@log_call
# /Users/user/github.com/getcher123/MyHomeGeBot/utils/telegrammy/telegram_bot.py
def make_message_correct(text: str, *,
                         MAX_MESSAGE_LENGTH=200
                         ) -> str:
    """
    Makes a given message correct by removing any special characters and shortening it if necessary.

    :param text: The text to make correct.
    :return: The corrected text.

    >>> TelegramBot.make_message_correct("This message contains $pecial characters and is too long to be sent to Telegram.")
    'This message contains pecial characters and is too long to be sent to Telegram'
    >>> TelegramBot.make_message_correct("This message is too long to be sent to Telegram.")
    'This message is too long to be sent to Telegram'
    """
    # Remove any special characters
    corrected_text = re.sub('[^a-zA-Z0-9_ ]', '', text)

    # Shorten the message if necessary
    if len(corrected_text) > MAX_MESSAGE_LENGTH:
        corrected_text = corrected_text[:MAX_MESSAGE_LENGTH]

    return corrected_text
