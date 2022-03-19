from .auxiliary import _filter
from .video import Video
from .channel import Channel
from .playlist import Playlist
from .videobulk import _VideoBulk
from .channelbulk import _ChannelBulk
from .playlistbulk import _PlaylistBulk
from ._rgxs import _QueryPatterns as rgx
from ._http import _find_videos, _find_channels, _find_playlists


class Search:

    def __init__(self):
        pass

    @staticmethod
    def video(keywords: str) -> Video:
        """
        :return: < video object > regarding the query
        """
        video_ids = rgx.video_id.findall(_find_videos(keywords))
        return Video(video_ids[0]) if video_ids else None

    @staticmethod
    def channel(keywords: str) -> Channel:
        """
        :return: < channel object > regarding the query
        """
        channel_ids = rgx.channel_id.findall(_find_channels(keywords))
        return Channel(channel_ids[0]) if channel_ids else None

    @staticmethod
    def playlist(keywords: str) -> Playlist:
        """
        :return: < playlist object > regarding the query
        """
        playlist_ids = rgx.playlist_id.findall(_find_playlists(keywords))
        return Playlist(found[0]) if found else None

    @staticmethod
    def videos(keywords: str, limit: int = 20) -> _VideoBulk:
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of videos to be searched
        :return: list of < video object > of each video regarding the query (consider limit)
        """
        video_ids = rgx.video_id.findall(_find_videos(keywords))
        pure_list = _filter(limit=limit, iterable=video_ids)
        return _VideoBulk(pure_list) if pure_list else None

    @staticmethod
    def channels(keywords: str, limit: int = 20) -> _ChannelBulk:
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of channels to be searched
        :return: list of < channel object > of each video regarding the query (consider limit)
        """
        channel_ids = rgx.channel_id.findall(_find_channels(keywords))
        pure_list = _filter(limit=limit, iterable=channel_ids)
        return _ChannelBulk(pure_list) if pure_list else None

    @staticmethod
    def playlists(keywords: str, limit: int = 20) -> _PlaylistBulk:
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total playlists be searched
        :return: list of < playlist object > of each playlist regarding the query (consider limit)
        """
        playlist_ids = rgx.playlist_id.findall(_find_playlists(keywords))
        pure_list = _filter(limit=limit, iterable=playlist_ids)
        return _PlaylistBulk(pure_list) if pure_list else None
