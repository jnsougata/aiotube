import re
import urllib.request
from .__proc__ import _duration


class Video:

    def __init__(self, videoId: str):

        """

        :param videoId: video id or the url of the video

        """

        if len(videoId) > 15:

            if 'watch?v=' in videoId:
                self.url = videoId
                self.id = re.findall(r"v=(.*)", videoId)[0]

            elif 'youtu.be/' in videoId:
                idL = re.findall(r"youtu\.be/(.*)", videoId)
                self.url = f'https://www.youtube.com/watch?v={idL[0]}'
                self.id = re.findall(r"/(.*)", videoId)[0]
        else:
            self.url = f'https://www.youtube.com/watch?v={videoId}'
            self.id = videoId

    @property
    def title(self):

        """

        :return: the title of the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"title\":\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def views(self):

        """

        :return: total views the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"", raw
        )
        return data[0] if len(data) != 0 else None

    @property
    def likes(self):

        """

        :return: total likes the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"label\":\"(.*?) likes\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def dislikes(self):

        """

        :return: total dislikes the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )
        return data[0] if len(data) != 0 else None

    @property
    def duration(self):

        """

        :return: total duration of  the video in milliseconds

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"approxDurationMs\":\"(.*?)\"", raw)

        return _duration(int(int(data[0]) / 1000)) if len(data) != 0 else None

    @property
    def upload_date(self):

        """

        :return: the date on which the video has been uploaded

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"uploadDate\":\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def parent(self):

        """

        :return: the id of the channel from which the video belongs

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"channelIds\":\[\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def description(self):

        """

        :return: description provided with the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable", raw)
        return data[0] if len(data) != 0 else None

    @property
    def thumbnail(self):

        """

        :return: url of the thumbnail of the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        return data[0] if len(data) != 0 else None

    @property
    def tags(self):

        """

        :return: list of tags used in video meta-data

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)
        return data[0].split(',') if len(data) != 0 else None

    @property
    def info(self):

        """

        :return: dict containing the the whole info of the video

        dict = {

            'title':title_data,
            'id':self.id,
            'views':views_data,
            'likes':likes_data,
            'dislikes':dislikes_data,
            'duration':duration_data,
            'parent':id_data,
            'uploaded':date_data,
            'url':self.url,
            'thumbnail':thumb_data,
            'tags':tags,
        }

        """

        raw = urllib.request.urlopen(self.url).read().decode()

        title_data = re.findall(r"\"title\":\"(.*?)\"", raw)

        v_data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"", raw
        )

        likes_data_list = re.findall(r"\"label\":\"(.*?) likes\"", raw)

        dislikes_data_list = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )

        duration_data_list = re.findall(r"approxDurationMs\":\"(.*?)\"", raw)

        id_data_list = re.findall(r"channelIds\":\[\"(.*?)\"", raw)

        date_data_list = re.findall(r"uploadDate\":\"(.*?)\"", raw)

        thumb_data_list = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        tags_data_list = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)

        infoDict = {
            'title': title_data[0] if len(title_data) != 0 else None,
            'id': self.id,
            'views': v_data[0] if len(v_data) != 0 else None,
            'likes': likes_data_list[0] if len(likes_data_list) != 0 else None,
            'dislikes': dislikes_data_list[0] if len(dislikes_data_list) != 0 else None,
            'parent': id_data_list[0] if len(id_data_list) != 0 else None,
            'duration': _duration(int(int(duration_data_list[0]) / 1000)) if len(duration_data_list) != 0 else None,
            'uploaded': date_data_list[0] if len(date_data_list) != 0 else None,
            'url': self.url,
            'thumbnail': thumb_data_list[0] if len(thumb_data_list) != 0 else None,
            'tags': tags_data_list[0].split(',') if len(tags_data_list) != 0 else None,
        }

        return infoDict