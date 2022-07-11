from urllib.request import urlopen
from collections import OrderedDict
from urllib.error import HTTPError, URLError
from .errors import TooManyRequests, InvalidURL, AIOError


__all__ = ['dup_filter', 'parser']


def _fetch_webpage(url: str):

    try:
        return urlopen(url).read().decode()
    except HTTPError as e:
        if e.code == 404:
            raise InvalidURL('can not find anything with the requested url') from None
        if e.code == 429:
            raise TooManyRequests('you are being rate-limited for sending too many requests') from None
    except Exception as e:
        raise AIOError(f'{e!r}') from None


def dup_filter(iterable: list, limit: int = None) -> list:
    if iterable:
        lim = limit if limit else len(iterable)
        converted = list(OrderedDict.fromkeys(iterable))
        if len(converted) - lim > 0:
            return converted[:-len(converted) + lim]
        else:
            return converted
    return []


def parser(kw: str):
    return kw.replace(" ", '+')
