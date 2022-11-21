from urllib.request import Request, urlopen
from collections import OrderedDict
from urllib.error import HTTPError, URLError
from .errors import TooManyRequests, InvalidURL, AIOError
from .pool import collect


__all__ = ['dup_filter', 'parser', 'request']


def request(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
    }
    req = Request(url, headers=headers)
    try:
        return urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        if e.code == 404:
            raise InvalidURL('can not find anything with the requested url')
        if e.code == 429:
            raise TooManyRequests('you are being rate-limited for sending too many requests')
    except Exception as e:
        raise AIOError(f'{e!r}') from None


def dup_filter(iterable: list, limit: int = None) -> list:
    if not iterable:
        return []
    lim = limit if limit else len(iterable)
    converted = list(OrderedDict.fromkeys(iterable))
    if len(converted) - lim > 0:
        return converted[:-len(converted) + lim]
    else:
        return converted


def parser(kw: str):
    return kw.replace(" ", '+')
