from typing import Dict, Tuple

from home_parser import MyHomeParser
from utils import log, log_call

Url = str


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


def convert_int(var, val):
    try:
        price_val = int(val)
    except:  # fixme ?n
        log.exception(f"Error <{var}> convert! {val = }")
    else:
        return price_val


def get_price_val(price):
    return convert_int('price',
                       price
                       .replace('м2', '')
                       .replace(' ', '')
                       )


@log_call
def get_price_2_sqr_val(price, square):
    price_val = get_price_val(price)
    square_val = convert_int('square', square)
    price_2_sqr_val = '<unknown>' if not all((price_val, price_val)) else square_val / price_val
    return price_2_sqr_val


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

    tags_txt = get_tags_txt(full_descr_info, price=price, address=address)

    add_info = (
        f"\n"
        f"price-to-square: {get_price_2_sqr_val(price, square)}"
        f"\n"
        f"{tags_txt}"
    )

    return (f"{full_descr_info}"
            f" \n"
            f"{add_info}"
            )
