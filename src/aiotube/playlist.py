from ._threads import _Thread
from .utils import filter
from .videobulk import VideoBulk
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx
from typing import List, Optional, Dict, Any


class Playlist:

    __HEAD = 'https://www.youtube.com/playlist?list='

    def __init__(self, playlist_id: str):
        """
        :param str playlist_id: the _id of the playlist
        """
        if 'youtube.com' in playlist_id:
            self.id = playlist_id.split('list=')[-1]
        else:
            self.id = playlist_id

        self.__playlist_data = _get_playlist_data(self.id)

    def __repr__(self):
        return f'<Playlist {self.url}>'


    @property
    def name(self) -> Optional[str]:
        """
        :return: the name of the playlist
        """
        names = rgx.name.findall(self.__playlist_data)
        return names[0] if names else None

    @property
    def url(self) -> Optional[str]:
        """
        :return: url of the playlist
        """
        return f'https://www.youtube.com/playlist?list={self.id}'

    @property
    def video_count(self) -> Optional[str]:
        """
        :return: total number of videos in that playlist
        """
        video_count = rgx.video_count.findall(self.__playlist_data)
        return video_count[0] if video_count else None

    @property
    def videos(self) -> VideoBulk:
        """
        :return: list of < video objects > for each video in the playlist (consider limit)
        """

        videos = rgx.video_id.findall(self.__playlist_data)
        return VideoBulk(filter(iterable=videos))

    @property
    def thumbnail(self) -> Optional[str]:
        """
        :return: url of the thumbnail of the playlist
        """
        thumbnails = rgx.thumbnail.findall(self.__playlist_data)
        return thumbnails[0] if thumbnails else None
    
    @property
    def info(self) -> Dict[str, Any]:
        """
        :return: a dict containing playlist info
        """

        def _get_data(pattern):
            data = pattern.findall(self.__playlist_data)
            return data[0] if data else None

        patterns = [rgx.name, rgx.video_count, rgx.thumbnail]

        data = _Thread.run(_get_data, patterns)

        return {
            'name': data[0],
            'video_count': data[1],
            'videos': filter(rgx.video_id.findall(raw)),
            'url': self.__HEAD + self.id,
            'thumbnail': data[2]
        }
        