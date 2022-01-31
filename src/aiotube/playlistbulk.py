import re
from .auxiliary import _src
from ._threads import _Thread


class _PlaylistBulk:

    def __init__(self, iterable: list):
        self._ls = iterable

    @property
    def ids(self):
        return self._ls

    @property
    def urls(self):
        head = 'https://www.youtube.com/playlist?list='
        return [f'{head}{item}' for item in self._ls]

    @property
    def _sources(self):
        def get_page(url):
            return _src(url)
        return _Thread.run(get_page, self.urls)

    @property
    def names(self):
        pattern = r"title\":\"(.*?)\""
        return [re.findall(pattern, item)[0] for item in self._sources]

    @property
    def video_counts(self):
        pattern = r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def thumbnails(self):
        pattern = r"og:image\" content=\"(.*?)\?"
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]
