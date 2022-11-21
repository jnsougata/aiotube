import re
import json
from .https import video_data
from typing import Dict, Any


class Video:

    _HEAD = 'https://www.youtube.com/watch?v='

    def __init__(self, video_id: str):
        pattern = re.compile('.be/(.*?)$|=(.*?)$|^(\w{11})$')
        self._matched_id = (
                pattern.search(video_id).group(1)
                or pattern.search(video_id).group(2)
                or pattern.search(video_id).group(3)
        )
        if self._matched_id:
            self._url = self._HEAD + self._matched_id
            self._video_data = video_data(self._matched_id)
        else:
            raise ValueError('invalid video id or url')

    def __repr__(self):
        return f'<Video {self._url}>'

    @property
    def metadata(self) -> Dict[str, Any]:
        details_pattern = re.compile('videoDetails\":(.*?)\"isLiveContent\":.*?}')
        upload_date_pattern = re.compile("<meta itemprop=\"uploadDate\" content=\"(.*?)\">")
        genre_pattern = re.compile("<meta itemprop=\"genre\" content=\"(.*?)\">")
        like_count_pattern = re.compile("iconType\":\"LIKE\"},\"defaultText\":(.*?)}}")
        raw_details = details_pattern.search(self._video_data).group(0)
        upload_date = upload_date_pattern.search(self._video_data).group(1)
        metadata = json.loads(raw_details.replace('videoDetails\":', ''))
        data = {
            'title': metadata['title'],
            'id': metadata['videoId'],
            'views': metadata.get('viewCount'),
            'streamed': metadata['isLiveContent'],
            'duration': metadata['lengthSeconds'],
            'author_id': metadata['channelId'],
            'upload_date': upload_date,
            'url': f"https://www.youtube.com/watch?v={metadata['videoId']}",
            'thumbnails': metadata.get('thumbnail', {}).get('thumbnails'),
            'tags': metadata.get('keywords'),
            'description': metadata.get('shortDescription'),
        }
        try:
            likes_count = like_count_pattern.search(self._video_data).group(1)
            data['likes'] = json.loads(likes_count + '}}}')[
                'accessibility'
            ]['accessibilityData']['label'].split(' ')[0].replace(',', '')
        except (AttributeError, KeyError):
            data['likes'] = None
        try:
            data['genre'] = genre_pattern.search(self._video_data).group(1)
        except AttributeError:
            data['genre'] = None
        return data
