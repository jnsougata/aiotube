import re
from .https import (
    channel_about,
    channel_live_data,
    old_streams,
    uploads_data,
    channel_playlists,
    video_count,
    upcoming_videos
)
from .video import Video
from .pool import collect
from .utils import dup_filter
from urllib.parse import unquote
from typing import List, Optional, Dict, Any
from .patterns import _ChannelPatterns as Patterns


class Channel:

    _HEAD = 'https://www.youtube.com/channel/'
    _CUSTOM = 'https://www.youtube.com/c/'

    def __init__(self, channel_id: str):
        if channel_id.startswith(self._HEAD):
            self._target_url = channel_id
            self._usable_id = channel_id.replace(self._HEAD, '')
        elif channel_id.startswith(self._CUSTOM):
            self._target_url = channel_id
            self._usable_id = channel_id.replace(self._CUSTOM, '')
        elif channel_id.startswith('UC'):
            self._target_url = self._HEAD + channel_id
            self._usable_id = channel_id
        else:
            self._target_url = self._CUSTOM + channel_id
            self._usable_id = channel_id
        self._about_page = channel_about(self._target_url)

    def __repr__(self):
        return f'<Channel `{self._target_url}`>'

    @property
    def metadata(self) -> Optional[Dict[str, any]]:
        patterns = [
            Patterns.name,
            Patterns.subscribers,
            Patterns.views,
            Patterns.creation,
            Patterns.country,
            Patterns.custom_url,
            Patterns.avatar,
            Patterns.banner,
            Patterns.id,
            Patterns.verified,
            Patterns.description,
            Patterns.links
        ]
        ext = collect(lambda x: x.findall(self._about_page) or None, patterns)
        data = [e[0] if e else None for e in ext]
        views = data[2].split(' ')[0] if data[2] else None
        custom_url = data[5] if '/channel/' not in str(data[5]) else None
        return {
            'id': data[8],
            'name': data[0],
            'subscribers': data[1],
            'verified': data[9] is not None,
            'views': views,
            'created_at': data[3],
            'country': data[4],
            'custom_url': custom_url,
            'avatar': data[6],
            'banner': data[7],
            'url': "https://www.youtube.com/channel/" + data[8],
            'description': str(data[10]).replace('\\n', '\n'),
            'socials': ['https://' + unquote(link) for link in list(set(ext[11]))] if data[11] else None
        }

    def live(self) -> bool:
        check = Patterns.live.findall(channel_live_data(self._target_url))
        return True if Patterns.check_live.search(check[0]) else False

    def streaming_now(self) -> Video:
        raw = channel_live_data(self._target_url)
        check = Patterns.live.findall(raw)
        if check and Patterns.check_live.search(check[0]):
            video_id = dup_filter(Patterns.video_id.findall(raw))[0]
            return Video(video_id)

    def current_streams(self) -> Optional[List[str]]:
        raw = channel_live_data(self._target_url)
        check = Patterns.live.findall(raw)
        if check and Patterns.check_live.search(check[0]):
            return dup_filter(Patterns.video_id.findall(raw))

    def old_streams(self) -> Optional[List[str]]:
        raw = old_streams(self._target_url)
        return dup_filter(Patterns.video_id.findall(raw))

    def uploads(self, limit: int = 20) -> Optional[List[Video]]:
        return dup_filter(Patterns.uploads.findall(uploads_data(self._target_url)), limit)

    def playlists(self) -> Optional[List[str]]:
        raw = channel_playlists(self._target_url)
        return dup_filter(Patterns.playlists.findall(raw))

    def video_count(self) -> Optional[str]:
        if self._usable_id.startswith('UC'):
            q_term = self._usable_id
        else:
            q_term = self.id
        count = Patterns.video_count.findall(video_count(q_term))
        return count[0].replace(',', '').replace('"', '').split()[0] if count else None

    def last_uploaded(self) -> Optional[Video]:
        raw = uploads_data(self._target_url)
        chunk = Patterns.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if not Patterns.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not Patterns.upload_chunk_fl_2.search(data)]
        return Video(Patterns.video_id.findall(fl_2[0])[0]) if fl_2 else None

    def last_streamed(self) -> Optional[Video]:
        raw = uploads_data(self._target_url)
        chunk = Patterns.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if Patterns.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not Patterns.upload_chunk_fl_2.search(data)]
        return Video(Patterns.video_id.findall(fl_2[0])[0]) if fl_2 else None

    def upcoming(self) -> Optional[Video]:
        raw = upcoming_videos(self._target_url)
        if not Patterns.upcoming_check.search(raw):
            return None
        upcoming = Patterns.upcoming.findall(raw)
        return Video(upcoming[0]) if upcoming else None

    def upcomings(self) -> Optional[List[str]]:
        raw = upcoming_videos(self._target_url)
        if not Patterns.upcoming_check.search(raw):
            return None
        video_ids = Patterns.upcoming.findall(raw)
        return video_ids
