from ._threads import _Thread
from ._http import _get_channel_about
from ._rgxs import _ChannelPatterns as rgx


class _ChannelBulk:

    def __init__(self, iterable: list):
        self._channel_ids = iterable

    @property
    def ids(self):
        return self._channel_ids

    @property
    def urls(self):
        return [f'https://www.youtube.com/channel/' + channel_id for channel_id in self._channel_ids]
    
    @property
    def _sources(self):

        def fetch_bulk_source(url):
            return _get_channel_about(url)

        return _Thread.run(fetch_bulk_source, self.urls)
        
    @property
    def names(self):
        return [rgx.name.findall(data)[0] for data in self._sources]

    @property
    def subscribers(self):
        temp = [rgx.subscribers.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def views(self):
        temp = [rgx.views.findall(data) for data in self._sources]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def created_ats(self):
        temp = [rgx.creation.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]
        
    @property
    def countries(self):
        temp = [rgx.country.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def custom_urls(self):
        temp = [rgx.custom_url.findall(data) for data in self._sources]
        return [item[0] if '/channel/' not in item[0] else None for item in temp]

    @property
    def descriptions(self):
        temp = [rgx.description.findall(data) for data in self._sources]
        return [item[0].replace('\\n', '\n') if item else None for item in temp]

    @property
    def avatars(self):
        temp = [rgx.avatar.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def banners(self):
        temp = [rgx.banner.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def verifieds(self):
        return [True if rgx.verified.search(data) else False for data in self._sources]

    @property
    def live_nows(self):
        pattern = r'{"text":" watching"}'
        return [True if re.search(pattern, item) else False for item in self._sources]
