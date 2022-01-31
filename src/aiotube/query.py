import re
from .video import Video
from .channel import Channel
from .playlist import Playlist
from .videobulk import _VideoBulk
from .channelbulk import _ChannelBulk
from .playlistbulk import _PlaylistBulk
from .auxiliary import _parser, _filter, _src


class Search:

    def __init__(self):
        pass

    @staticmethod
    def video(keywords: str):
        """
        :return: < video object > regarding the query
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAQ%253D%253D')
        video_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        return Video(video_ids[0]) if video_ids else None

    @staticmethod
    def channel(keywords: str):
        """
        :return: < channel object > regarding the query
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAg%253D%253D')
        channel_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        return Channel(channel_ids[0]) if channel_ids else None

    @staticmethod
    def videos(keywords: str, limit: int):
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of videos to be searched
        :return: list of < video object > of each video regarding the query (consider limit)
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAQ%253D%253D')
        raw_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        pure_list = _filter(limit=limit, iterable=raw_ids)
        return _VideoBulk(pure_list) if pure_list else None

    @staticmethod
    def channels(keywords: str, limit: int):
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of channels to be searched
        :return: list of < channel object > of each video regarding the query (consider limit)
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAg%253D%253D')
        raw_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        pure_list = _filter(limit=limit, iterable=raw_ids)
        return _ChannelBulk(pure_list) if pure_list else None

    @staticmethod
    def playlist(keywords: str):
        """
        :return: < playlist object > regarding the query
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAw%253D%253D')
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        return Playlist(found[0]) if found else None

    @staticmethod
    def playlists(keywords: str, limit: int):
        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total playlists be searched
        :return: list of < playlist object > of each playlist regarding the query (consider limit)
        """
        raw = _src(f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAw%253D%253D')
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        pure = _filter(limit=limit, iterable=found)
        return _PlaylistBulk(pure) if pure else None
