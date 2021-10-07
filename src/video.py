import re
import requests
import urllib.request
from .threads import _HyperThread
from .auxiliary import _duration, _audio_steam, _video_stream

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
            format: str,
            filename: str = None,
    ):

        if filename:
            prefix = filename.replace(' ', '')
        else:
            prefix = 'aiofile'



        if format == 'mp3':
            try:
                stream = _audio_steam(self._id)
                if stream:
                    r = requests.get(stream, stream=True)

                    print(f'Downloading [ {self._id} ]')

                    with open(f"{prefix}_{self._id}.mp3", "wb") as file:
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                file.write(chunk)

                        print(f'Completed [ {self._id} ]')
                        print(f'file path: {prefix}_{self._id}.mp3\n----------')
                        return f"{prefix}_{self._id}.mp3"
                else:
                    raise RuntimeError('unable to retrieve file')
            except:
                raise RuntimeError('unable to download file')

        elif format == 'mp4':
            try:
                stream = _video_stream(self._id)
                if stream:
                    r = requests.get(stream, stream=True)

                    print(f'Downloading [ {self._id} ]')

                    with open(f"{prefix}_{self._id}.mp4", "wb") as file:
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                file.write(chunk)

                        print(f'Completed [ {self._id} ]')
                        print(f'file path: {prefix}_{self._id}.mp4\n----------')
                        return f"{prefix}_{self._id}.mp4"
                else:
                    raise RuntimeError('unable to retrieve file')
            except:
                raise RuntimeError('unable to download file')

        else:
            raise ValueError("invalid format. use mp3 or mp4")


    @property
    def chunks(self):
        """
        :return: returns music file in bytes form
        """
        stream = _audio_steam(self._id)
        if stream:
            return urllib.request.urlopen(stream).read()


    @property
    def downloads(self):
        return _audio_steam(self._id), _video_stream(self._id)
