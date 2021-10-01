import re
import youtube_dl
import urllib.request
from .__proc__ import _duration
from .__hyp__ import _HyperThread


class Video:

    def __init__(self, videoId: str):

        """
        :param videoId: video id or the url of the video
        """

        if 'watch?v=' in videoId:
            self._url = videoId
            self._id = re.findall(r"v=(.*)", videoId)[0]

        elif 'youtu.be/' in videoId:
            idL = re.findall(r"youtu\.be/(.*)", videoId)
            self._url = f'https://www.youtube.com/watch?v={idL[0]}'
            self._id = re.findall(r"/(.*)", videoId)[0]
        else:
            self._url = f'https://www.youtube.com/watch?v={videoId}'
            self._id = videoId


    @property
    def url(self):
        return self._url


    @property
    def id(self):
        return self._id


    @property
    def title(self):

        """
        :return: the title of the video
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"\"title\":\"(.*?)\"", raw)
        return data[0] if len(data) > 0 else None


    @property
    def views(self):

        """
        :return: total views the video got so far
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"",
            raw
        )
        return data[0][:-6] if len(data) > 0 else None


    @property
    def likes(self):

        """
        :return: total likes the video got so far
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(
            r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) ",
            raw
        )
        return data[0] if len(data) > 0 else None


    @property
    def dislikes(self):

        """
        :return: total dislikes the video got so far
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )
        return data[0] if len(data) > 0 else None


    @property
    def duration(self):

        """
        :return: total duration of  the video in 00h 00m 00s
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"approxDurationMs\":\"(.*?)\"", raw)

        return _duration(int(int(data[0]) / 1000)) if len(data) > 0 else None


    @property
    def upload_date(self):

        """
        :return: the date on which the video has been uploaded
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"uploadDate\":\"(.*?)\"", raw)
        return data[0] if len(data) > 0 else None


    @property
    def parent(self):

        """
        :return: the id of the channel from which the video belongs
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"channelIds\":\[\"(.*?)\"", raw)
        return data[0] if len(data) > 0 else None


    @property
    def description(self):

        """
        :return: description provided with the video
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable", raw)
        return data[0].replace('\\n', '') if len(data) > 0 else None


    @property
    def thumbnail(self):

        """
        :return: _url of the thumbnail of the video
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        return data[0] if len(data) > 0 else None


    @property
    def tags(self):

        """
        :return: list of tags used in video meta-data
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)
        return data[0].split(',') if len(data) > 0 else None


    @property
    def info(self):

        """
        :return: dict containing the the whole info of the video

        dict = {

            'title': -> str,
            'id': -> str,
            'views': -> str,
            'likes': -> str,
            'dislikes': -> str,
            'duration': -> str,
            'parent': -> str,
            'uploaded': -> str,
            'url': -> str,
            'thumbnail': -> str,
            'tags': -> list,
        }
        """

        raw = urllib.request.urlopen(self._url).read().decode()

        def _get_data(pattern):
            data = re.findall(pattern, raw)
            return data[0] if len(data) > 0 else None

        patterns = [

            r"\"title\":\"(.*?)\"",
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"",
            r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) ",
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            r"approxDurationMs\":\"(.*?)\"",
            r"channelIds\":\[\"(.*?)\"",
            r"uploadDate\":\"(.*?)\"",
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            r"<meta name=\"keywords\" content=\"(.*?)\">"

        ]

        ls = _HyperThread.run(_get_data, patterns)


        infoDict = {

            'title': ls[0],
            'id': self._id,
            'views': ls[1][:-6],
            'likes': ls[2],
            'dislikes': ls[3],
            'duration': _duration(int(int(ls[4]) / 1000)),
            'parent': ls[5],
            'uploaded': ls[6],
            'url': self._url,
            'thumbnail': ls[7],
            'tags': ls[8].split(','),

        }

        return infoDict


    def download(
            self,
            filename:str = None,
            audio:bool = None,
            video:bool = None
    ):
        if filename:
            name = filename.replace(' ','')
        else:
            name = 'aiofile'

        def _file(aud, vid):
            try:
                if aud and not vid:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl':f'downloads/{name}_{self.id}.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                    return ydl_opts

                elif vid and not aud:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': f'downloads/{name}_{self.id}.%(ext)s',
                    }
                    return ydl_opts

            except UnboundLocalError:
                return None

        options = _file(audio, video)

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([self._id])
