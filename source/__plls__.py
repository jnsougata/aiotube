import re
import urllib.request
from .__vid__ import Video
from .__proc__ import _filter


class Playlist:
    def __init__(self, playlist_id: str):

        """

        :param str playlist_id: the _id of the playlist

        """

        if 'youtube.com' in playlist_id:
            self.id = re.findall(r'=(.*)', playlist_id)[0]
        else:
            self.id = playlist_id


    @property
    def info(self):

        """

        :return: a dict containing playlist info

        dict = {
                'name': -> str,
                'url': -> str,
                'video_count': -> int,
                'videos': -> bulk,
                'thumbnail': -> str,
            }

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'

        raw = urllib.request.urlopen(url).read().decode()

        name_data = re.findall(r"{\"title\":\"(.*?)\"", raw)

        video_count_data = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"", raw)

        thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)

        data_dict = {

            'name': name_data[0] if len(name_data) != 0 else None,
            'url': f'https://www.youtube.com/playlist?list={self.id}',
            'video_count': video_count_data[0] if len(video_count_data) != 0 else None,
            'videos': _filter(re.findall(r"videoId\":\"(.*?)\"", raw)),
            'thumbnail': thumbnails[0] if len(thumbnails) != 0 else None,
        }

        return data_dict

    @property
    def name(self):

        """

        :return: the name of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        name_data = re.findall(r"{\"title\":\"(.*?)\"", raw)
        return name_data[0] if len(name_data) != 0 else None

    @property
    def url(self):

        """

        :return: url of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        return url

    @property
    def video_count(self):

        """

        :return: total number of videos in that playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        video_count = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"", raw)
        return video_count[0] if len(video_count) != 0 else None

    def videos(self, limit: int = None):

        """

        :param int limit: number of videos the user want from the playlist
        :return: list of < video objects > for each video in the playlist (consider limit)

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        videos = re.findall(r"videoId\":\"(.*?)\"", raw)
        pure = _filter(limit=limit, iterable=videos)
        return [Video(item) for item in pure]

    @property
    def thumbnail(self):

        """

        :return: url of the thumbnail of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)
        return thumbnails[0] if len(thumbnails) != 0 else None