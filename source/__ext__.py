import re
import urllib.request
from .__vid__ import Video
from .__proc__ import _filter
from .__vidbulk__ import _VideoBulk


class Extras:

    def __init__(self):
        pass



    @property
    def Trending(self):

        """

        :return: < video object > of #1 on trending video

        """

        url = f'https://www.youtube.com/feed/trending'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return Video(data[0]) if len(data) != 0 else None


    @property
    def Music(self):

        """

        :return: list of < video object > of trending music videos

        """

        url = f'https://www.youtube.com/feed/music'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None


    @property
    def Gaming(self):

        """

        :return: list of < video object > of trending gaming videos

        """

        url = f'https://www.youtube.com/gaming'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None


    @property
    def News(self):

        """

        :return: list of < video object > of trending news videos

        """

        url = f'https://www.youtube.com/news'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None

    @property
    def Live(self):

        """

        :return: list of < video object > of trending livestreams

        """

        url = f'https://www.youtube.com/live'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None

    @property
    def Learning(self):

        """

        :return: list of < video object > of trending educational videos

        """

        url = f'https://www.youtube.com/learning'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None


    @property
    def Sports(self):

        """

        :return: list of < video object > of trending sports videos

        """
        url = f'https://www.youtube.com/sports'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return _VideoBulk(_filter(data)) if len(data) > 0 else None