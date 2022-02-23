import re
from ._threads import _Thread
from .auxiliary import _src, _duration


class _VideoBulk:

    def __init__(self, iterable: list):
        self._ls = iterable

    @property
    def _sources(self):
        head = 'https://www.youtube.com/watch?v='
        urls = [f'{head}{item}/about' for item in self._ls]

        def get_page(url):
            return _src(url)

        return _Thread.run(get_page, urls)

    @property
    def ids(self):
        return self._ls

    @property
    def urls(self):
        head = 'https://www.youtube.com/watch?v='
        return [f'{head}{item}' for item in self._ls]

    @property
    def titles(self):
        pattern = r"title\":\"(.*?)\""
        return [re.findall(pattern, item)[0] for item in self._sources]

    @property
    def views(self):
        pattern = r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def likes(self):
        pattern = r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) "
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]


    @property
    def durations(self):
        pattern = r"approxDurationMs\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [_duration(int(int(item[0]) / 1000)) if item else None for item in temp]

    @property
    def upload_dates(self):
        pattern = r"uploadDate\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def authors(self):
        pattern = r"channelIds\":\[\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def descriptions(self):
        pattern = r"shortDescription\":\"(.*)\",\"isCrawlable"
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0].replace('\\n', ' ') if item else None for item in temp]

    @property
    def thumbnails(self):
        pattern = r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def tags(self):
        pattern = r"<meta name=\"keywords\" content=\"(.*?)\">"
        temp = [re.findall(pattern, item) for item in self._sources]
        return [item[0].split(',') if item else None for item in temp]
