from ._http import _get_video_data
from ._threads import _Thread
from ._rgxs import _VideoPatterns as rgx
from typing import List, Optional, Dict, Any


class _VideoBulk:

    def __init__(self, iterable: list):
        self._video_ids = iterable
        self.__source_data = self.__fetch_all

    @property
    def __fetch_all(self):

        def fetch_bulk_source(video_id):
            return _get_video_data(video_id)

        return _Thread.run(fetch_bulk_source, self._video_ids)

    @staticmethod
    def _get_info(source: str) -> Dict[str, Any]:
        """
        :return: dict containing the whole info of the video
        """

        def _get_data(pattern):
            data = pattern.findall(source)
            return data[0] if data else None

        patterns = [
            rgx.title, rgx.views, rgx.likes, rgx.duration, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description,
            rgx.is_streamed, rgx.is_premiered, rgx.video_id
        ]

        data = _Thread.run(_get_data, patterns)

        return {
            'title': data[0],
            'id': data[11],
            'views': data[1][:-6] if data[1] else None,
            'likes': data[2],
            'duration': int(data[3]) / 1000 if data[3] else None,
            'author': data[4],
            'upload_date': data[5],
            'url': f'https://www.youtube.com/watch?v={data[11]}',
            'thumbnail': data[6],
            'tags': data[7].split(','),
            'streamed': True if data[9] else False,
            'premiered': True if data[10] else False,
            'description': data[8].replace('\\n', '\n') if data[8] else None,
        }

    def _gen_bulk(self) -> Dict[str, Dict[str, Any]]:
        bulk = {}
        for src in self.__source_data:
            __info__ = self._get_info(src)
            __id__ = __info__['id']
            bulk[__id__] = __info__
        return bulk
