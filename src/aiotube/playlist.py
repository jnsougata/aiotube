from ._threads import _Thread
from .utils import dup_filter
from .videobulk import _VideoBulk
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx
from typing import List, Optional, Dict, Any


class Playlist:

    def __init__(self, playlist_id: str):
        if 'youtube.com' in playlist_id:
            self.id = playlist_id.split('list=')[-1]
        else:
            self.id = playlist_id

        self.__playlist_data = _get_playlist_data(self.id)

    def __repr__(self):
        return f'<Playlist {self.url}>'

    @property
    def name(self) -> Optional[str]:
        names = rgx.name.findall(self.__playlist_data)
        return names[0] if names else None

    @property
    def url(self) -> Optional[str]:
        return f'https://www.youtube.com/playlist?list={self.id}'

    @property
    def video_count(self) -> Optional[str]:
        video_count = rgx.video_count.findall(self.__playlist_data)
        return video_count[0] if video_count else None

    @property
    def videos(self) -> _VideoBulk:
        videos = rgx.video_id.findall(self.__playlist_data)
        return _VideoBulk(dup_filter(iterable=videos))

    @property
    def thumbnail(self) -> Optional[str]:
        thumbnails = rgx.thumbnail.findall(self.__playlist_data)
        return thumbnails[0] if thumbnails else None
    
    @property
    def info(self) -> Dict[str, Any]:
        info = {}

        def _get_data(pattern):
            d = pattern.findall(self.__playlist_data)
            return d[0] if d else None

        patterns = [rgx.name, rgx.video_count, rgx.thumbnail]

        data = _Thread.run(_get_data, patterns)

        info['id'] = self.id
        info['name'] = data[0]
        info['video_count'] = data[1]
        info['thumbnail'] = data[2]
        info['url'] = self.url
        info['videos'] = dup_filter(rgx.video_id.findall(raw))

        return info
        