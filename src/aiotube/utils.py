import urllib3
from collections import OrderedDict
from urllib.error import HTTPError, URLError
from .errors import TooManyRequests, InvalidURL, BadURL, AIOError


__all__ = ['filter', 'duration', 'parser']


def create_http_pool(pool_size=1):
    http = urllib3.PoolManager(num_pools=pool_size)
    return http


def _src(url: str):
    """
    :param url: url to be requested
    :return: the requested page
    """
    http = create_http_pool()
    try:
        return http.request('GET', url).data.decode('utf-8')
    except HTTPError as error:
        if error.code == 404:
            raise InvalidURL('can not find anything the requested url')
        if error.code == 429:
            raise TooManyRequests('sending too many requests in a short period of time')
    except URLError:
        raise BadURL('bad url format used')
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
