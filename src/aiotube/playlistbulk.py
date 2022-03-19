from ._threads import _Thread
from .utils import filter
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx
from typing import List


class PlaylistBulk:

    def __init__(self, iterable: list):
        self._playlist_ids = iterable

    @property
    def ids(self) -> List[str]:
        return self._playlist_ids

    @property
    def urls(self) -> List[str]:
        head = 'https://www.youtube.com/playlist?list='
        return [head + pl_id for pl_id in self._playlist_ids]

    @property
    def _sources(self):

        def fetch_bulk_source(playlist_id):
            return _get_playlist_data(playlist_id)

        return _Thread.run(fetch_bulk_source, self.ids)

    @property
    def names(self) -> List[str]:
        temp = [rgx.name.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def video_counts(self) -> List[str]:
        temp = [rgx.video_count.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def thumbnails(self) -> List[str]:
        temp = [rgx.thumbnail.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def video_ids(self) -> List[List[str]]:
        return [filter(rgx.video_id.findall(data)) for data in self._sources]
