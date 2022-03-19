from ._http import _get_video_data
from ._threads import _Thread
from ._rgxs import _VideoPatterns as rgx
from typing import List


class VideoBulk:

    def __init__(self, iterable: list):
        self._video_ids = iterable

    @property
    def _sources(self):

        def fetch_bulk_source(video_id):
            return _get_video_data(video_id)

        return _Thread.run(fetch_bulk_source, self.ids)

    @property
    def ids(self) -> List[str]:
        return self._video_ids

    @property
    def urls(self) -> List[str]:
        head = 'https://www.youtube.com/watch?v='
        return [head + video_id for video_id in self._video_ids]

    @property
    def titles(self) -> List[str]:
        temp = [rgx.title.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def views(self) -> List[str]:
        temp = [rgx.views.findall(data) for data in self._sources]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def likes(self) -> List[str]:
        temp = [rgx.likes.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]


    @property
    def durations(self) -> List[float]:
        temp = [rgx.duration.findall(data) for data in self._sources]
        return [int(item[0]) / 1000 if item else None for item in temp]

    @property
    def upload_dates(self) -> List[str]:
        temp = [rgx.upload_date.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def authors(self) -> List[str]:
        temp = [rgx.author_id.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def descriptions(self) -> List[str]:
        temp = [rgx.description.findall(data) for data in self._sources]
        return [item[0].replace('\\n', '\n') if item else None for item in temp]

    @property
    def thumbnails(self) -> List[str]:
        temp = [rgx.thumbnail.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def tags(self) -> List[List[str]]:
        temp = [rgx.tags.findall(data) for data in self._sources]
        return [item[0].split(',') if item else None for item in temp]
