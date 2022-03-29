from ._threads import _Thread
from ._http import _get_channel_about
from ._rgxs import _ChannelPatterns as rgx
from typing import List, Optional, Dict, Any


class _ChannelBulk:

    __HEAD = 'https://www.youtube.com/channel/'

    def __init__(self, iterable: list):
        self._channel_ids = iterable
        self.__bulk_data = self.__fetch_all


    @property
    def __fetch_all(self):
        urls = [self.__HEAD + id for id in self._channel_ids]
        return _Thread.run(_get_channel_about, urls)


    def _gen_bulk(self):
        bulk = {}
        for src in self.__bulk_data:
            __info__ = self._extract_info(src)
            __id__ = __info__['id']
            bulk[__id__] = self._extract_info(src)
        return bulk

    @staticmethod
    def _extract_info(source: str) -> Optional[Dict[str, Dict[str, Any]]]:

        def extract(pattern):
            data = pattern.findall(source)
            return data[0] if data else None

        patterns = [
            rgx.name, rgx.subscribers, rgx.views, rgx.creation,
            rgx.country, rgx.custom_url, rgx.avatar, rgx.banner, rgx.id,
            rgx.verified, rgx.description
        ]

        data = _Thread.run(extract, patterns)

        if data[2]:
            views = data[2].split(' ')[0]
        else:
            views = None

        curl = data[5] if data[5] and '/channel/' not in data[5] else None
        url = 'https://www.youtube.com/channel/' + data[8]

        return {
            'name': data[0],
            'id': data[8],
            'verified': True if data[9] else False,
            'subscribers': data[1],
            'views': views,
            'created_at': data[3],
            'country': data[4],
            'url': url,
            'custom_url': curl,
            'avatar': data[6],
            'banner': data[7],
            'description': data[10].replace('\\n', '\n').replace('\n', ' ').replace('\\', ' ') if data[10] else None
        }
