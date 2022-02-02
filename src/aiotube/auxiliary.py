import urllib.request
from urllib.error import HTTPError, URLError
from collections import OrderedDict
from .errors import TooManyRequests, InvalidURL, BadURL, AIOError


__all__ = ['_src', '_filter', '_duration', '_parser']


def _src(url: str):
    """
    :param url: url to be requested
    :return: the requested page
    """
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode()
    except HTTPError as error:
        if error.code == 404:
            raise InvalidURL('can not find anything the requested url')
        if error.code == 429:
            raise TooManyRequests('sending too many requests in a short period of time')
    except URLError:
        raise BadURL('bad url format used')
    except Exception as error:
        raise AIOError(f'{error}')


def _filter(iterable: list, limit: int = None) -> list:
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
    else:
        return []


def _duration(seconds: int):
    """
    :param seconds: duration to be converted
    :return: a duration string with 00h 00m 00s format
    """
    dur_hour = int(seconds // 3600)
    dur_min = int((seconds % 3600) // 60)
    dur_sec = int(seconds - (3600 * dur_hour) - (60 * dur_min))
    return f'{dur_hour}h {dur_min}m {dur_sec}s'


def _parser(kw: str):
    return kw.replace(" ", '+')
