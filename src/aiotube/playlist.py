import re
from ._threads import _Thread
from .auxiliary import _filter
from .videobulk import VideoBulk
from ._http import _get_playlist_data
from ._rgxs import _PlaylistPatterns as rgx


class Playlist:
    def __init__(self, playlist_id: str):
        """
        :param str playlist_id: the _id of the playlist
        """
        if 'youtube.com' in playlist_id:
            self.id = re.findall(r'=(.*)', playlist_id)[0]
        else:
            self.id = playlist_id

    @property
    def name(self):
        """
        :return: the name of the playlist
        """
        raw = _get_playlist_data(self.id)
        names = rgx.name.findall(raw)
        return names[0] if names else None

    @property
    def url(self):
        """
        :return: url of the playlist
        """
        return f'https://www.youtube.com/playlist?list={self.id}'

    @property
    def video_count(self):
        """
        :return: total number of videos in that playlist
        """
        raw = _get_playlist_data(self.id)
        video_count = rgx.video_count.findall(raw)
        return video_count[0] if video_count else None

    @property
    def videos(self):
        """
        :return: list of < video objects > for each video in the playlist (consider limit)
        """

        raw = _get_playlist_data(self.id)
        videos = rgx.video_id.findall(raw)
        return VideoBulk(_filter(iterable=videos))

    @property
    def thumbnail(self):
        """
        :return: url of the thumbnail of the playlist
        """
        raw = _get_playlist_data(self.id)
        thumbnails = rgx.thumbnail.findall(raw)
        return thumbnails[0] if thumbnails else None
    
    @property
    def info(self):
        """
        :return: a dict containing playlist info
        """
        raw = _get_playlist_data(self.id)

        def _get_data(pattern):
            data = pattern.findall(raw)
            return data[0] if data else None

        patterns = [rgx.name, rgx.video_count, rgx.thumbnail]

        data = _Thread.run(_get_data, patterns)

        return {
            'name': data[0],
            'video_count': data[1],
            'videos': _filter(rgx.video_id.findall(raw)),
            'url': f'https://www.youtube.com/playlist?list={self.id}',
            'thumbnail': data[2]
        }
        