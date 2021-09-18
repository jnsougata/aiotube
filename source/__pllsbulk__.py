import re
import urllib.request as req
from .__hyp__ import _HyperThread



class _PlaylistBulk:

    def __init__(self, iterable: list):
        self._ls = iterable

    @property
    def name(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"{\"title\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/playlist?list={item}' for item in self._ls])


    @property
    def url(self):
        return [f'https://www.youtube.com/playlist?list={item}' for item in self._ls]

    @property
    def video_count(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/playlist?list={item}' for item in self._ls])

    @property
    def thumbnail(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"og:image\" content=\"(.*?)\?"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/playlist?list={item}' for item in self._ls])