from urllib.request import urlopen
from collections import OrderedDict
from urllib.error import HTTPError, URLError
from .errors import TooManyRequests, InvalidURL, BadURL, AIOError


__all__ = ['filter', 'parser']


def _fetch_webpage(url: str):

    try:
        return urlopen(url).read().decode()
    except HTTPError as e:
        if e.code == 404:
            raise InvalidURL('can not find anything with the requested url')
        if e.code == 429:
            raise TooManyRequests('you are being ratelimited for sending too many requests')
    except URLError:
        raise BadURL('url does not match any supported format')
    except Exception as e:
        raise AIOError(f'{e!r}')


def filter(iterable: list, limit: int = None) -> list:
    """
    Restricts element repetition in iterable
    :param int limit: number of desired elements
    :param iterable: list or tuple of elements
    :return: modified list (consider limit)
    """
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
