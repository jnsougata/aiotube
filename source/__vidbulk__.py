import re
import urllib.request as req
from .__proc__ import _duration
from .__hyp__ import _HyperThread



class _VideoBulk:

    def __init__(self, iterable:list):
        self._ls = iterable

    @property
    def title(self):

        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"title\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def views(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\""
            views = re.findall(pattern, raw)
            return views[0][:-6] if len(views) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def likes(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) "
            likes = re.findall(pattern, raw)
            return likes[0] if len(likes) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def dislikes(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\""
            dislikes = re.findall(pattern, raw)
            return dislikes[0] if len(dislikes) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def duration(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"approxDurationMs\":\"(.*?)\""
            duration = re.findall(pattern, raw)
            return _duration(int(int(duration[0]) / 1000))

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def upload_date(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"uploadDate\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def parent(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"channelIds\":\[\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def description(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"shortDescription\":\"(.*)\",\"isCrawlable"
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def thumbnail(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def tags(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"<meta name=\"keywords\" content=\"(.*?)\">"
            tags = re.findall(pattern, raw)
            return tags[0].split(',') if len(tags) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/watch?v={item}' for item in self._ls])


    @property
    def url(self):
        return [f'https://www.youtube.com/watch?v={item}' for item in self._ls]


    @property
    def id(self):
        return self._ls