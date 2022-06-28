from ._threads import _Thread
from .utils import dup_filter
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx
from typing import List, Dict, Any


class _PlaylistBulk:

    def __init__(self, iterable: list):
        self._playlist_ids = iterable
        self.__bulk = self.__fetch_all()

    def __fetch_all(self):

        def fetch_bulk_source(playlist_id):
            return _get_playlist_data(playlist_id)

        return _Thread.run(fetch_bulk_source, self._playlist_ids)

    @staticmethod
    def _get_info(source: str) -> Dict[str, Any]:
        info = {}

        def _get_data(pattern):
            d = pattern.findall(source)
            return d[0] if d else None

        patterns = [rgx.name, rgx.video_count, rgx.thumbnail]

        data = _Thread.run(_get_data, patterns)

        info['name'] = data[0]
        info['video_count'] = data[1]
        info['thumbnail'] = data[2]
        info['url'] = None
        info['videos'] = dup_filter(rgx.video_id.findall(source))

        return info

    def _gen_bulk(self) -> Dict[str, Dict[str, Any]]:
        info_list = []
        for pl_data in self.__bulk:
            info = self._get_info(pl_data)
            for pl_id in self._playlist_ids:
                if pl_id in pl_data:
                    info['id'] = pl_id
                    info['url'] = f'https://www.youtube.com/playlist?list={pl_id}'
            info_list.append(info)

        return {info.pop('id'): info for info in info_list}
