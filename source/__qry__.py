import re
import urllib.request
from .__vid__ import Video
from .__ch__ import Channel
from .__plls__ import Playlist
from .__vidbulk__ import _VideoBulk
from .__chbulk__ import _ChannelBulk
from .__proc__ import _parser, _filter
from .__pllsbulk__ import _PlaylistBulk


class Search:

    def __init__(self):
        pass



    @classmethod
    def video(cls, keywords:str):

        """

        :return: < video object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        video_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        return Video(video_ids[0]) if len(video_ids) != 0 else None


    @classmethod
    def channel(cls, keywords:str):

        """

        :return: < channel object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        channel_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        return Channel(channel_ids[0]) if len(channel_ids) != 0 else None


    @classmethod
    def videos(cls, keywords:str, limit: int = None):

        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of videos to be searched
        :return: list of < video object > of each video regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        pureList = _filter(limit=limit, iterable=raw_ids)
        return _VideoBulk(pureList) if len(pureList) != 0 else None


    @classmethod
    def channels(cls, keywords:str, limit: int = None):

        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total number of channels to be searched
        :return: list of < channel object > of each video regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        pureList = _filter(limit=limit, iterable=raw_ids)
        return _ChannelBulk(pureList) if len(pureList) != 0 else None


    @classmethod
    def playlist(cls, keywords:str):

        """

        :return: < playlist object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAw%253D%253D'
        raw = urllib.request.urlopen(url=url).read().decode()
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        return Playlist(found[0]) if len(found) != 0 else None


    @classmethod
    def playlists(cls, keywords:str, limit: int = None):

        """
        :param str keywords: query to be searched on YouTube
        :param int limit: total playlists be searched
        :return: list of < playlist object > of each playlist regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={_parser(keywords)}&sp=EgIQAw%253D%253D'
        raw = urllib.request.urlopen(url=url).read().decode()
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        pure = _filter(limit = limit, iterable = found)
        return _PlaylistBulk(pure) if len(pure) != 0 else None