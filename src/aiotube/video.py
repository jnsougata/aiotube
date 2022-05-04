from ._threads import _Thread
from ._http import _get_video_data
from ._rgxs import _VideoPatterns as rgx
from typing import List, Optional, Dict, Any


class Video:

    __HEAD = 'https://www.youtube.com/watch?v='

    def __init__(self, video_id: str):

        if 'watch?v=' in video_id:
            ids = video_id.split('=')
            self._id = ids[-1]
            self._url = video_id

        elif 'youtu.be/' in video_id:
            ids = video_id.split('/')
            self._id = ids[-1]
            self._url = self.__HEAD + self._id

        else:
            self._id = video_id
            self._url = self.__HEAD + self._id

        self.__video_data = _get_video_data(self._id)

    def __repr__(self):
        if self.id:
            return f'<Video {self.url}>'
        return f'<Invalid Video Object>'

    @property
    def url(self) -> str:
        return self._url

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> Optional[str]:

        data = rgx.title.findall(self.__video_data)
        return data[0] if data else None

    @property
    def views(self) -> Optional[str]:

        data = rgx.views.findall(self.__video_data)
        return data[0][:-6] if data else None

    @property
    def likes(self) -> Optional[str]:

        data = rgx.likes.findall(self.__video_data)
        return data[0] if data else None

    @property
    def duration(self) -> Optional[float]:

        data = rgx.duration.findall(self.__video_data)
        return int(data[0]) / 1000 if data else None

    @property
    def upload_date(self) -> Optional[str]:

        data = rgx.upload_date.findall(self.__video_data)
        return data[0] if data else None

    @property
    def author(self) -> Optional[str]:

        data = rgx.author_id.findall(self.__video_data)
        return data[0] if data else None

    @property
    def description(self) -> Optional[str]:

        data = rgx.description.findall(self.__video_data)
        return data[0].replace('\\n', '\n') if data else None

    @property
    def thumbnail(self) -> Optional[str]:

        data = rgx.thumbnail.findall(self.__video_data)
        return data[0] if data else None

    @property
    def tags(self) -> Optional[List[str]]:

        data = rgx.tags.findall(self.__video_data)
        return data[0].split(',') if data else None

    @property
    def streamed(self) -> bool:
        if rgx.is_streamed.search(self.__video_data):
            return True
        return False

    @property
    def premiered(self) -> bool:
        if rgx.is_premiered.search(self.__video_data):
            return True
        return False

    @property
    def info(self) -> Dict[str, Any]:

        def _get_data(pattern):
            value = pattern.findall(self.__video_data)
            return value[0] if value else None

        patterns = [
            rgx.title, rgx.views, rgx.likes, rgx.duration, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description,
            rgx.is_streamed, rgx.is_premiered
        ]

        data = _Thread.run(_get_data, patterns)

        return {
            'title': data[0],
            'id': self._id,
            'views': data[1][:-6] if data[1] else None,
            'likes': data[2],
            'duration': int(data[3]) / 1000 if data[3] else None,
            'author': data[4],
            'upload_date': data[5],
            'url': self._url,
            'thumbnail': data[6],
            'tags': data[7].split(','),
            'streamed': True if data[9] else False,
            'premiered': True if data[10] else False,
            'description': data[8].replace('\\n', '\n') if data[8] else None,
        }
