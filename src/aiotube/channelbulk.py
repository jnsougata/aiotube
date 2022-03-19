from ._threads import _Thread
from ._http import _get_channel_about
from ._rgxs import _ChannelPatterns as rgx
from typing import List


class ChannelBulk:

    def __init__(self, iterable: list):
        self._channel_ids = iterable

    @property
    def ids(self):
        return self._channel_ids

    @property
    def urls(self) -> List[str]:
        return [f'https://www.youtube.com/channel/' + channel_id for channel_id in self._channel_ids]
    
    @property
    def _sources(self):

        def fetch_bulk_source(url):
            return _get_channel_about(url)

        return _Thread.run(fetch_bulk_source, self.urls)
        
    @property
    def names(self) -> List[str]:
        return [rgx.name.findall(data)[0] for data in self._sources]

    @property
    def subscribers(self) -> List[str]:
        temp = [rgx.subscribers.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def views(self) -> List[str]:
        temp = [rgx.views.findall(data) for data in self._sources]
        return [item[0][:-6] if item else None for item in temp]

    @property
    def created_ats(self) -> List[str]:
        temp = [rgx.creation.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]
        
    @property
    def countries(self) -> List[str]:
        temp = [rgx.country.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def custom_urls(self) -> List[str]:
        temp = [rgx.custom_url.findall(data) for data in self._sources]
        return [item[0] if '/channel/' not in item[0] else None for item in temp]

    @property
    def descriptions(self) -> List[str]:
        temp = [rgx.description.findall(data) for data in self._sources]
        return [item[0].replace('\\n', '\n') if item else None for item in temp]

    @property
    def avatars(self) -> List[str]:
        temp = [rgx.avatar.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def banners(self) -> List[str]:
        temp = [rgx.banner.findall(data) for data in self._sources]
        return [item[0] if item else None for item in temp]

    @property
    def verifieds(self) -> List[bool]:
        return [True if rgx.verified.search(data) else False for data in self._sources]

    @property
    def live_nows(self) -> List[bool]:
        return [True if rgx.live.search(data) else False for data in self._sources]
