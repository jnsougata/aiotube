from .utils import filter
from typing import Optional
from .video import Video
from .channel import Channel
from .playlist import Playlist
from .videobulk import VideoBulk
from .channelbulk import ChannelBulk
from .playlistbulk import PlaylistBulk
from ._rgxs import _QueryPatterns as rgx
from ._http import _find_videos, _find_channels, _find_playlists


class Search:


    @staticmethod
    def video(keywords: str) -> Optional[Video]:
        video_ids = rgx.video_id.findall(_find_videos(keywords))
        return Video(video_ids[0]) if video_ids else None

    @staticmethod
    def channel(keywords: str) -> Optional[Channel]:
        channel_ids = rgx.channel_id.findall(_find_channels(keywords))
        return Channel(channel_ids[0]) if channel_ids else None

    @staticmethod
    def playlist(keywords: str) -> Optional[Playlist]:
        playlist_ids = rgx.playlist_id.findall(_find_playlists(keywords))
        return Playlist(found[0]) if found else None

    @staticmethod
    def videos(keywords: str, limit: int = 20) -> Optional[VideoBulk]:
        video_ids = rgx.video_id.findall(_find_videos(keywords))
        pure_list = filter(limit=limit, iterable=video_ids)
        return VideoBulk(pure_list) if pure_list else None

    @staticmethod
    def channels(keywords: str, limit: int = 20) -> Optional[ChannelBulk]:
        channel_ids = rgx.channel_id.findall(_find_channels(keywords))
        pure_list = filter(limit=limit, iterable=channel_ids)
        return ChannelBulk(pure_list) if pure_list else None

    @staticmethod
    def playlists(keywords: str, limit: int = 20) -> Optional[PlaylistBulk]:
        playlist_ids = rgx.playlist_id.findall(_find_playlists(keywords))
        pure_list = filter(limit=limit, iterable=playlist_ids)
        return PlaylistBulk(pure_list) if pure_list else None
