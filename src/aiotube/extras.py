from ._http import (
    _get_trending_video,
    _get_trending_songs,
    _get_trending_gaming_videos,
    _get_trending_news_feeds,
    _get_trending_streams,
    _get_trending_learning_videos,
    _get_trending_sports_videos
)
from .video import Video
from .utils import filter
from .videobulk import VideoBulk
from ._rgxs import _ExtraPatterns as rgx



class Extras:


    @staticmethod
    def trending():
        """
        :return: < video object > of #1 on trending video
        """
        data = rgx.video_id.findall(_get_trending_video())
        return Video(data[0]) if data else None

    @staticmethod
    def music():
        """
        :return: list of < video object > of trending music videos
        """
        data = rgx.video_id.findall(_get_trending_songs())
        return VideoBulk(filter(data)) if data else None

    @staticmethod
    def gaming():
        """
        :return: list of < video object > of trending gaming videos
        """
        data = rgx.video_id.findall(_get_trending_gaming_videos())
        return VideoBulk(filter(data)) if data else None

    @staticmethod
    def news():
        """
        :return: list of < video object > of trending news videos
        """
        data = rgx.video_id.findall(_get_trending_news_feeds())
        return VideoBulk(filter(data)) if data else None

    @staticmethod
    def livestreams():
        """
        :return: list of < video object > of trending livestreams
        """
        data = rgx.video_id.findall(_get_trending_streams())
        return VideoBulk(filter(data)) if data else None

    @staticmethod
    def learning():
        """
        :return: list of < video object > of trending educational videos
        """
        data = rgx.video_id.findall(_get_trending_learning_videos())
        return VideoBulk(filter(data)) if data else None

    @staticmethod
    def sports():
        """
        :return: list of < video object > of trending sports videos
        """
        data = rgx.video_id.findall(_get_trending_sports_videos())
        return VideoBulk(filter(data)) if data else None
