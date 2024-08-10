import json
import re
from collections import OrderedDict
from typing import Dict, Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .errors import TooManyRequests, InvalidURL, RequestError

__all__ = ["dup_filter", "request", "extract_initial_data"]


def request(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
    }
    req = Request(url, headers=headers)
    try:
        return urlopen(req).read().decode("utf-8")
    except HTTPError as e:
        if e.code == 404:
            raise InvalidURL("can not find anything with the requested url")
        if e.code == 429:
            raise TooManyRequests(
                "you are being rate-limited for sending too many requests"
            )
    except Exception as e:
        raise RequestError(f"{e!r}") from None


def dup_filter(iterable: list, limit: int = None) -> list:
    if not iterable:
        return []
    lim = limit if limit else len(iterable)
    converted = list(OrderedDict.fromkeys(iterable))
    if len(converted) - lim > 0:
        return converted[: -len(converted) + lim]
    else:
        return converted


def extract_initial_data(html: str) -> Dict[str, Any]:
    pattern = re.compile("ytInitialData = {(.+?)};")
    results = pattern.finditer(html)
    return json.loads("{" + results.__next__().group(1) + "}")
