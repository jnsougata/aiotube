import re
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
    def _sources(self):
        head = 'https://www.youtube.com/channel/'
        urls = [f'{head}{item}/about' for item in self._ls]
        def get_page(url):
            return _src(url)
        return _Thread.run(get_page, urls)
        
    @property
    def names(self):
        srcs = self._sources
        pattern = r"channelMetadataRenderer\":{\"title\":\"(.*?)\""
        return [re.findall(pattern, item)[0] for item in srcs]

    @property
    def subscribers(self):
        srcs = self._sources
        pattern = r"}},\"simpleText\":\"(.*?) "
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if item else None for item in temp]

    @property
    def views(self):
        srcs = self._sources
        pattern = r"viewCountText\":{\"simpleText\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def joined(self):
        srcs = self._sources
        pattern = r"text\":\"Joined \"},{\"text\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if item else None for item in temp]
        
    @property
    def countries(self):
        srcs = self._sources
        pattern = r"country\":{\"simpleText\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if item else None for item in temp]

    @property
    def custom_urls(self):
        srcs = self._sources
        pattern = r"canonicalChannelUrl\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if '/channel' not in item[0] else None for item in temp]

    @property
    def descriptions(self):
        srcs = self._sources
        pattern = r"description\":{\"simpleText\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0].replace('\\n', ' ') if item else None for item in temp]


    @property
    def avatars(self):
        srcs = self._sources
        pattern = "height\":88},{\"url\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if item else None for item in temp]

    @property
    def banners(self):
        srcs = self._sources
        pattern = r"width\":1280,\"height\":351},{\"url\":\"(.*?)\""
        temp = [re.findall(pattern, item) for item in srcs]
        return [item[0] if item else None for item in temp]

    @property
    def verifieds(self):
        srcs = self._sources
        pattern = 'label":"Verified'
        return [True if re.search(pattern, item) else False for item in srcs]

    @property
    def lives(self):
        srcs = self._sources
        pattern = r'{"text":" watching"}'
        return [True if re.search(pattern, item) else False for item in srcs]