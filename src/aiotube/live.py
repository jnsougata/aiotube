import re
from ._threads import _Thread
from .auxiliary import _src


class Live:

    def __init__(self, video_id: str):
        """
        :param video_id: video id or the url of the video
        """
        if 'watch?v=' in video_id:
            self._url = video_id
            self._id = re.findall(r"v=(.*)", video_id)[0]

        elif 'youtu.be/' in video_id:
            id_list = re.findall(r"youtu\.be/(.*)", video_id)
            self._url = f'https://www.youtube.com/watch?v={id_list[0]}'
            self._id = re.findall(r"/(.*)", video_id)[0]
        else:
            self._url = f'https://www.youtube.com/watch?v={video_id}'
            self._id = video_id

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
        raw = _src(self._url)
        data = re.findall(r"\"title\":\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def views(self):
        """
        :return: total views the video got so far
        """
        raw = _src(self._url)
        data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"",
            raw
        )
        return data[0][:-6] if data else None

    @property
    def likes(self):
        """
        :return: total likes the video got so far
        """
        raw = _src(self._url)
        data = re.findall(
            r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) ",
            raw
        )
        return data[0] if data else None

    @property
    def dislikes(self):
        raise DeprecationWarning("This property is deprecated as YouTube is slowly removing public dislike counts.")


    @property
    def upload_date(self):
        """
        :return: the date on which the video has been uploaded
        """
        raw = _src(self._url)
        data = re.findall(r"uploadDate\":\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def author(self):
        """
        :return: the id of the channel from which the video belongs
        """
        raw = _src(self._url)
        data = re.findall(r"channelIds\":\[\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def description(self):
        """
        :return: description provided with the video
        """
        raw = _src(self._url)
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable", raw)
        return data[0].replace('\\n', '') if data else None

    @property
    def thumbnail(self):
        """
        :return: _url of the thumbnail of the video
        """
        raw = _src(self._url)
        data = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        return data[0] if data else None

    @property
    def tags(self):
        """
        :return: list of tags used in video meta-data
        """
        raw = _src(self._url)
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)
        return data[0].split(',') if data else None

    @property
    def info(self):
        """
        :return: dict containing the whole info of the video
        dict = {

            'title': -> str,
            'id': -> str,
            'views': -> str,
            'likes': -> str,
            'dislikes': -> str,
            'duration': -> str,
            'author': -> str,
            'uploaded': -> str,
            'url': -> str,
            'thumbnail': -> str,
            'tags': -> list,
        }
        """
        raw = _src(self._url)

        def _get_data(pattern):
            data = re.findall(pattern, raw)
            return data[0] if len(data) > 0 else None

        patterns = [

            r"\"title\":\"(.*?)\"",
            r"toggledText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) ",
            r"approxDurationMs\":\"(.*?)\"",
            r"author\":\"(.*?)\"",
            r"uploadDate\":\"(.*?)\"",
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            r"<meta name=\"keywords\" content=\"(.*?)\">"

        ]

        ls = _Thread.run(_get_data, patterns)

        return {

            'title': ls[0],
            'id': self._id,
            'views': ls[1],
            'likes': ls[2],
            'duration': None,
            'author': ls[3],
            'upload_date': ls[4],
            'url': self._url,
            'thumbnail': ls[5],
            'tags': ls[6].split(',') if ls[6] else None,
        }
