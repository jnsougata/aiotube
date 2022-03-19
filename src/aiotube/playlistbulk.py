from ._threads import _Thread
from .auxiliary import _filter
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx


class _PlaylistBulk:

    def __init__(self, iterable: list):
        self._playlist_ids = iterable

    @property
    def ids(self):
        return self._playlist_ids

    @property
    def urls(self):
        head = 'https://www.youtube.com/playlist?list='
        return [head + pl_id for pl_id in self._playlist_ids]

    @property
    def _sources(self):

        def fetch_bulk_source(url):
            return _get_playlist_data(url)

        return _Thread.run(fetch_bulk_source, self.urls)

    @property
    def names(self):
        return [rgx.name.findall(data)[0] for data in self._sources]

    @property
    def video_counts(self):
        temp = [rgx.video_count.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def thumbnails(self):
        temp = [rgx.thumbnail.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def video_ids(self):
        return [_filter(rgx.video_id.findall(data)) for data in self._sources]
