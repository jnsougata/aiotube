from .video import Video
from ._threads import _Thread
from ._http import _get_video_data
from ._rgxs import _VideoPatterns as rgx


class Live(Video):

    def __init__(self, video_id: str):
        super().__init__(video_id)

    @property
    def duration(self) -> float:
        return 0.0

    @property
    def streamed(self) -> bool:
        return True

    @property
    def info(self) -> dict:
        """
        :return: dict containing the whole info of the video
        """
        raw = _get_video_data(self._id)

        def _get_data(pattern):
            data = pattern.findall(raw)
            return data[0] if len(data) > 0 else None

        patterns = [
            rgx.title, rgx.views, rgx.likes, rgx.duration, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description
        ]

        data = _Thread.run(_get_data, patterns)

        return {
            'title': data[0],
            'id': self._id,
            'views': data[1][:-6] if data[1] else None,
            'likes': data[2],
            'duration': self.duration,
            'author': data[4],
            'upload_date': data[5],
            'url': self._url,
            'thumbnail': data[6],
            'tags': data[7].split(','),
            'description': data[8].replace('\\n', '\n') if data[8] else None,
            'streamed': self.streamed,
        }
