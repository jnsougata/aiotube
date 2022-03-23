from .video import Video
from ._http import _get_video_data
from typing import Optional, Dict, Any
from ._rgxs import _VideoPatterns as rgx


class Upcoming(Video):

    def __init__(self, video_id: str):
        super().__init__(video_id)

    def duration(self) -> float:
        return 0.0

    def views(self) -> Optional[str]:
        return None

    @property
    def info(self) -> Dict[str, Any]:
        """
        :return: dict containing the whole info of the video
        """
        raw = _get_video_data(self._id)

        def _get_data(pattern):
            data = pattern.findall(raw)
            return data[0] if len(data) > 0 else None

        patterns = [
            rgx.title, rgx.likes, rgx.author_id,
            rgx.upload_date, rgx.thumbnail, rgx.tags, rgx.description
        ]

        data = _Thread.run(_get_data, patterns)

        description = data[6].replace('\\n', '\n') if data[6] else None

        return {
            'title': data[0],
            'id': self._id,
            'views': None,
            'likes': data[1],
            'duration': None,
            'author': data[2],
            'upload_date': data[3],
            'url': self._url,
            'thumbnail': data[4],
            'tags': data[5].split(','),
            'description': description,
        }
