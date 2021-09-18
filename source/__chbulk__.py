import re
import urllib.request as req
from .__hyp__ import _HyperThread



class _ChannelBulk:

    def __init__(self, iterable:list):
        self._ls = iterable

    @property
    def id(self):
        return self._ls


    @property
    def url(self):
        return [f'https://www.youtube.com/channel/{item}' for item in self._ls]


    @property
    def name(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"channelMetadataRenderer\":{\"title\":\"(.*?)\""
            return re.findall(pattern, raw)[0]

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def subscribers(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0][:-12] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def total_views(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0][:-6] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def joined(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def country(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"country\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def custom_url(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"\"canonicalChannelUrl\":\"(.*?)\""
            ins = re.findall(pattern, raw)
            temp = ins[0] if len(ins) > 0 else None
            return temp if '/channel' not in temp and temp is not None else None


        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def description(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"{\"description\":{\"simpleText\":\"(.*?)\"}"
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def avatar_url(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = "height\":88},{\"url\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def banner_url(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            pattern = r"width\":1280,\"height\":351},{\"url\":\"(.*?)\""
            temp = re.findall(pattern, raw)
            return temp[0] if len(temp) > 0 else None

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])


    @property
    def verified(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            isVerified = re.search(r'label":"Verified', raw)
            return True if isVerified else False

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])

    @property
    def live(self):
        def _get_data(url: str):
            raw = req.urlopen(url).read().decode()
            isLive = re.search(r'{"text":" watching"}', raw)
            return True if isLive else False

        return _HyperThread.run(_get_data, [f'https://www.youtube.com/channel/{item}/about' for item in self._ls])