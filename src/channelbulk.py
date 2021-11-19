import re
import urllib.request as req
from .auxiliary import _src
from .threads import _Thread



class _ChannelBulk:

    def __init__(self, iter:list):
        self._ls = iter

    @property
    def ids(self):
        return self._ls

    @property
    def urls(self):
        head = 'https://www.youtube.com/channel/'
        return [f'{head}{item}' for item in self._ls]
    
    @property
    def sources(self):
        head = 'https://www.youtube.com/channel/'
        urls = [f'{head}{item}/about' for item in self._ls]
        def get_page(url):
            return _src(url)
        return _Thread.run(get_page, urls)
        
    @property
    def names(self):
        srcs = self.sources
        pattern = r"channelMetadataRenderer\":{\"title\":\"(.*?)\""
        return [re.findall(pattern, item)[0] for item in srcs]

    @property
    def subscribers(self):
        srcs = self.sources
        pattern = r"}},\"simpleText\":\"(.*?) "
        return [re.findall(pattern, item)[0] if re.findall(pattern, item) else None for item in srcs]

    @property
    def views(self):
        srcs = self.sources
        pattern = r"viewCountText\":{\"simpleText\":\"(.*?)\""
        return [re.findall(pattern, item)[0][:-6] if re.findall(pattern, item) else None for item in srcs]

    @property
    def joined(self):
        srcs = self.sources
        pattern = r"text\":\"Joined \"},{\"text\":\"(.*?)\""
        return [re.findall(pattern, item)[0] if re.findall(pattern, item) else None for item in srcs]

    @property
    def countries(self):
        srcs = self.sources
        pattern = pattern = r"country\":{\"simpleText\":\"(.*?)\""
        return [re.findall(pattern, item)[0] if re.findall(pattern, item) else None for item in srcs]

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