from ._threads import _Thread
from .utils import filter
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx
from typing import List, Dict, Any


class _PlaylistBulk:

    def __init__(self, iterable: list):
        self._playlist_ids = iterable
        self.__bulk = self.__fetch_all


    @property
    def __fetch_all(self):

        def fetch_bulk_source(playlist_id):
            return _get_playlist_data(playlist_id)

        return _Thread.run(fetch_bulk_source, self._playlist_ids)


    @staticmethod
    def _get_info(source: str) -> Dict[str, Any]:

        def _get_data(pattern):
            data = pattern.findall(source)
            return data[0] if data else None

        patterns = [rgx.name, rgx.video_count, rgx.thumbnail]

        data = _Thread.run(_get_data, patterns)

        return {
            'name': data[0],
            'video_count': data[1],
            'videos': filter(rgx.video_id.findall(source)),
            'url': None,
            'thumbnail': data[2]
        }

    def _gen_bulk(self) -> Dict[str, Dict[str, Any]]:
        bulk = {}
        for src in self.__bulk:
            __info__ = self._get_info(src)
            for pl_id in self._playlist_ids:
                if pl_id in src:
                    __info__['url'] = f'https://www.youtube.com/playlist?list={pl_id}'
                    bulk[pl_id] = __info__
        return bulk
