import re
import urllib.request as req
from .threads import _Thread



class _ChannelBulk:

    def __init__(self, iterable:list):
        self._ls = iterable

    @property
    def ids(self):
        return self._ls


    @property
    def urls(self):
        head = 'https://www.youtube.com/channel/'
        return [f'{head}{item}' for item in self._ls]

    @property
    def names(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"channelMetadataRenderer\":{\"title\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def subscribers(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0][:-12] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def views(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0][:-6] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def joined(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def countries(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"country\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def custom_urls(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"canonicalChannelUrl\":\"(.*?)\""
            ins = re.findall(pattern, raw)
            temp = ins[0] if len(ins) > 0 else None
            return temp if '/channel' not in temp and temp is not None else None


        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def description(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"{\"description\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def avatar_urls(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = "height\":88},{\"url\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def banner_urls(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"width\":1280,\"height\":351},{\"url\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def verifieds(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            isVerified = re.search(r'label":"Verified', raw)
            return True if isVerified else False

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def lives(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            isLive = re.search(r'{"text":" watching"}', raw)
            return True if isLive else False

        return _Thread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])