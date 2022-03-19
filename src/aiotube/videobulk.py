from ._http import _get_video_data
from ._threads import _Thread
from .auxiliary import _duration
from ._rgxs import _VideoPatterns as rgx


class _VideoBulk:

    def __init__(self, iterable: list):
        self._video_ids = iterable

    @property
    def _sources(self):

        def fetch_bulk_source(url):
            return _get_video_data(url)

        return _Thread.run(fetch_bulk_source, self.urls)

    @property
    def ids(self):
        return self._video_ids

    @property
    def urls(self):
        head = 'https://www.youtube.com/watch?v='
        return [head + video_id for video_id in self._video_ids]

    @property
    def titles(self):
        return [rgx.title.findall(data)[0] for data in self._sources]

    @property
    def views(self):
        temp = [rgx.views.findall(data) for data in self._sources]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def likes(self):
        temp = [rgx.likes.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]


    @property
    def durations(self):
        temp = [rgx.duration.findall(data) for data in self._sources]
        return [_duration(int(int(item[0]) / 1000)) if item else None for item in temp]

    @property
    def upload_dates(self):
        temp = [rgx.upload_date.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def authors(self):
        temp = [rgx.author_id.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def descriptions(self):
        temp = [rgx.description.findall(data) for data in self._sources]
        return [item[0].replace('\\n', '\n') if item else None for item in temp]

    @property
    def thumbnails(self):
        temp = [rgx.thumbnail.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def tags(self):
        temp = [rgx.tags.findall(data) for data in self._sources]
        return [item[0].split(',') if item else None for item in temp]
