import re
from .video import Video
from .videobulk import _VideoBulk
from .auxiliary import _filter, _src


class Extras:

    def __init__(self):
        pass

    @property
    def trending(self):
        """
        :return: < video object > of #1 on trending video
        """
        raw = _src(f'https://www.youtube.com/feed/trending')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return Video(data[0]) if data else None

    @property
    def music(self):
        """
        :return: list of < video object > of trending music videos
        """
        raw = _src(f'https://www.youtube.com/feed/music')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None

    @property
    def gaming(self):
        """
        :return: list of < video object > of trending gaming videos
        """
        raw = _src(f'https://www.youtube.com/gaming')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None

    @property
    def news(self):
        """
        :return: list of < video object > of trending news videos
        """
        raw = _src(f'https://www.youtube.com/news')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None

    @property
    def livestream(self):
        """
        :return: list of < video object > of trending livestreams
        """
        raw = _src(f'https://www.youtube.com/live')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None

    @property
    def learning(self):
        """
        :return: list of < video object > of trending educational videos
        """
        raw = _src(f'https://www.youtube.com/learning')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None

    @property
    def sports(self):
        """
        :return: list of < video object > of trending sports videos
        """
        raw = _src(f'https://www.youtube.com/sports')
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if data else None
