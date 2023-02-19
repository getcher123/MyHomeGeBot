from home_parser import MyHomeParser
from utils import log, log_call

Url = str


@log_call
def get_tags_txt(full_desc_info: str, *, address: str = ''):
    address = address or full_desc_info.splitlines()[1]
    tags = []
    tags += address.split(' ')[-1]
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


@log_call
def get_price_2_sqr_val(price, square):
    price_val = convert_int('price',
                            price
                            .replace('м2', '')
                            .replace(' ', '')
                            )
    square_val = convert_int('square', square)
    price_2_sqr_val = '<unknown>' if not all((price_val, price_val)) else square_val / price_val
    return price_2_sqr_val


@log_call
def get_msg_txt(p: MyHomeParser, url: Url, i: int, *,
                prop_sep='     ',
                ):
    title = p.description['title'][i]
    price = p.description['price'][i]
    square = p.description['square'][i]
    descr = p.description['descr'][i]
    stairs = p.description['stairs'][i]
    address = p.description['address'][i]

    title = title

    price = price
    square = square.replace('.00', '')
    stairs = stairs.replace('Этаж', 'эт.')
    address = address.replace(', Батуми', '')
    descr = descr

    # i msg = f"**[{p.description['title'][i]}]({url})** - \n*${p.description['price'][i]}*     {p.description['square'][i]}     {p.description['stairs'][i]} \n{p.description['address'][i]}"
    full_descr_info = (f"**[{title}]({url})** -"
                       f" \n"
                       f"*${price}*"
                       f"{prop_sep}{square}"
                       f"{prop_sep}{stairs}"
                       f"{prop_sep}{descr}"
                       f" \n"
                       f"{address}")

    tags_txt = get_tags_txt(full_descr_info)
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
