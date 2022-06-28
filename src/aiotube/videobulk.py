from ._http import _get_video_data
from ._threads import _Thread
from ._rgxs import _VideoPatterns as rgx
from typing import List, Optional, Dict, Any


class _VideoBulk:

    def __init__(self, iterable: list):
        self._video_ids = iterable
        self.__source_data = self.__fetch_all()

    def __fetch_all(self):

        def fetch_bulk_source(video_id):
            return _get_video_data(video_id)

        return _Thread.run(fetch_bulk_source, self._video_ids)

    @staticmethod
    def _gen_info(source: str) -> Dict[str, Any]:
        info = {}

        def _get_data(pattern):
            d = pattern.findall(source)
            return d[0] if d else None

        patterns = [
            rgx.title, rgx.views, rgx.likes, rgx.duration, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description,
            rgx.is_streamed, rgx.is_premiered, rgx.video_id
        ]

        data = _Thread.run(_get_data, patterns)

        info['id'] = data[11]
        info['title'] = data[0]
        info['views'] = data[1]
        info['likes'] = data[2]
        info['duration'] = int(data[3]) / 1000 if data[3] else None
        info['author'] = data[4]
        info['upload_date'] = data[5]
        info['streamed'] = True if data[9] else False
        info['premiered'] = True if data[10] else False
        info['thumbnail'] = data[6]
        info['tags'] = data[7].split(',') if data[7] else None
        info['description'] = data[8].replace('\\n', '\n') if data[8] else None
        info['url'] = f'https://www.youtube.com/watch?v={data[11]}'

        return info

    def _gen_bulk(self) -> Dict[str, Dict[str, Any]]:
        info_list = [self._gen_info(source) for source in self.__source_data]
        return {info.pop('id'): info for info in info_list}
