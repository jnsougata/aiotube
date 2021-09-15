from collections import OrderedDict


def _filter(iterable:list, limit:int = None):
    """
    Restricts element repetition in iterable

    :param int limit: number of desired elements
    :param iterable: list or tuple of elements
    :return: modified list (consider limit)

    """
    lim = limit if limit is not None else 0
    converted = list(OrderedDict.fromkeys(iterable))
    return converted[:-len(converted) + lim] if len(converted) > len(converted) - lim > 0 else converted


def _duration(seconds: int):

    """
    :param seconds: duration to be converted
    :return: a duration string with 00h 00m 00s format

    """

    dur_hour = int(seconds // 3600)
    dur_min = int((seconds % 3600) // 60)
    dur_sec = int(seconds - (3600 * dur_hour) - (60 * dur_min))
    return f'{dur_hour}h {dur_min}m {dur_sec}s'


def _parser(kw:str):
    query = kw.replace(" ", '+')
    return query