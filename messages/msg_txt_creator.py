#todo: 4cg:
from typing import Dict, Tuple

from home_parser import MyHomeParser
from utils import log, log_call

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
    square_val = convert_int('square', square)
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
        # logd(f"{(prev, price) = }")
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

    return (f"{full_descr_info}"
            f" \n"
            f"{add_info}"
            )


#e1:
# t:# send_photo user_id = '40937921'
#
# 2023-02-19T18:11:37.300628+00:00 app[web.1]: DEBUG:aiogram:Make request: "sendPhoto" with data: "{'chat_id': '40937921', 'caption': "**[Улица А. Пушкина](https://www.myhome.ge/ru/pr/14441518/)** - \n*$600*     55 м²     эт. 10 \n \n\nprice-to-square: unsupported operand type(s) for /: 'NoneType' and 'int'\n#600_700", 'parse_mode': 'Markdown'}" and files "{'photo': <_io.BytesIO object at 0x7f53ff364950>}"
#
# 2023-02-19T18:11:37.338975+00:00 app[web.1]: DEBUG:aiogram:Response for sendPhoto: [400] "'{"ok":false,"error_code":400,"description":"Bad Request: can\'t parse entities: Can\'t find end of the entity starting at byte offset 191"}'"
#
# 2023-02-19T18:11:37.339556+00:00 app[web.1]: ERROR:root:Error while sending msg: **[Улица А. Пушкина](https://www.myhome.ge/ru/pr/14441518/)** - *$600* 55 м² эт. 10 price-to-square: unsupported operand type(s) for /: 'NoneType' and 'int' #600_700
#
# 2023-02-19T18:11:37.339556+00:00 app[web.1]: Traceback (most recent call last):
#
# 2023-02-19T18:11:37.339557+00:00 app[web.1]:   File "/app/messages/sender.py", line 35, in send_messages
#
# 2023-02-19T18:11:37.339558+00:00 app[web.1]:     await dp.bot.send_photo(user_id, photo=image_bytes_copy, caption=msg, parse_mode="Markdown")
#
# 2023-02-19T18:11:37.339559+00:00 app[web.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/aiogram/bot/bot.py", line 532, in send_photo
#
# 2023-02-19T18:11:37.339561+00:00 app[web.1]:     result = await self.request(api.Methods.SEND_PHOTO, payload, files)
#
# 2023-02-19T18:11:37.339561+00:00 app[web.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/aiogram/bot/base.py", line 231, in request
#
# 2023-02-19T18:11:37.339562+00:00 app[web.1]:     return await api.make_request(await self.get_session(), self.server, self.__token, method, data, files,
#
# 2023-02-19T18:11:37.339562+00:00 app[web.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/aiogram/bot/api.py", line 140, in make_request
#
# 2023-02-19T18:11:37.339562+00:00 app[web.1]:     return check_result(method, response.content_type, response.status, await response.text())
#
# 2023-02-19T18:11:37.339563+00:00 app[web.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/aiogram/bot/api.py", line 115, in check_result
#
# 2023-02-19T18:11:37.339563+00:00 app[web.1]:     exceptions.BadRequest.detect(description)
#
# 2023-02-19T18:11:37.339564+00:00 app[web.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/aiogram/utils/exceptions.py", line 140, in detect
#
# 2023-02-19T18:11:37.339570+00:00 app[web.1]:     raise err(cls.text or description)
#
# 2023-02-19T18:11:37.339571+00:00 app[web.1]: aiogram.utils.exceptions.CantParseEntities: Can't parse entities: can't find end of the entity starting at byte offset 191
#
# 2023-02-19T18:11:37.340303+00:00 app[web.1]: INFO:aiohttp.access:10.1.7.74 [19/Feb/2023:18:11:23 +0000] "POST /webhook/5619116931:AAE0CMs2SsA9J-isXDOdPIqKua1NaCQW9dQ HTTP/1.1" 200 172 "-" "-"
#
# 2023-02-19T18:11:37.332820+00:00 heroku[router]: at=info method=POST path="/webhook/5619116931:AAE0CMs2SsA9J-isXDOdPIqKua1NaCQW9dQ" host=myhomegebot-dev.herokuapp.com request_id=7f09fc40-1512-4ea7-891e-fe371166d2f1 fwd="91.108.6.152" dyno=web.1 connect=0ms service=13378ms status=200 bytes=172 protocol=https
#
# 2023-02-19T18:11:45.241099+00:00 app[web.1]: DEBUG:root:k.pop('len_tail_percent')=0.4 ignored!