from ._http import (
    _get_channel_about,
    _get_channel_live_data,
    _get_old_streams,
    _get_uploads_data,
    _get_channel_playlists,
    _get_video_count,
    _get_upcoming_videos
)
from typing import List, Optional, Dict, Any
from .live import Live
from .video import Video
from ._threads import _Thread
from urllib.parse import unquote
from .videobulk import VideoBulk
from .utils import filter
from .upcoming import Upcoming
from .playlistbulk import PlaylistBulk
from ._rgxs import _ChannelPatterns as rgx


class Channel:

    __HEAD = 'https://www.youtube.com/channel/'
    __CUSTOM = 'https://www.youtube.com/c/'

    def __init__(self, channel_id: str):
        """
        :param str channel_id: any of channel id, custom id, url , custom url
        """
        if channel_id.startswith('UC'):
            self._url = self.__HEAD + channel_id
        elif channel_id.startswith('http'):
            self._url = channel_id
        else:
            self._url = self.__CUSTOM + channel_id

        self.__given_id = channel_id
        self.__raw_about = _get_channel_about(self._url)

    def __repr__(self):
        if self.id:
            return f'<Channel {self.url}>'
        return '<Invalid Channel Object>'

    @property
    def name(self) -> Optional[str]:
        """
        :return: channel's name or None
        """
        name = rgx.name.findall(self.__raw_about)
        return name[0] if name else None

    @property
    def valid(self) -> bool:
        """
        :return: bool i.e. True if channel is valid else False
        """
        source = _src(self._url)
        return True if source else False

    @property
    def url(self) -> str:
        return self.__HEAD + self.id

    @property
    def id(self) -> str:
        """
        :return: the id of the channel
        """
        channel_id = rgx.id.findall(self.__raw_about)
        return channel_id[0] if channel_id else None

    @property
    def verified(self) -> bool:
        """
        :return: bool i.e. True if channel is verified else False
        """
        is_verified = rgx.verified.search(self.__raw_about)
        return True if is_verified else False

    @property
    def live(self) -> bool:
        """
        :return: channel's Live Status
        """
        check = rgx.live.findall(_get_channel_live_data(self._url))
        return True if rgx.check_live.search(check[0]) else False

    @property
    def livestream(self) -> Live:
        """
        :return: channel's ongoing  livestream url
        """
        raw = _get_channel_live_data(self._url)
        check = rgx.live.findall(raw)
        if check and rgx.check_live.search(check[0]):
            video_id = filter(rgx.video_id.findall(raw))[0]
            return Live(video_id)

    @property
    def livestreams(self) -> Optional[List[str]]:
        """
        :return: channel's ongoing  livestream urls
        """
        raw = _get_channel_live_data(self._url)
        check = rgx.live.findall(raw)
        if check and rgx.check_live.search(check[0]):
            return filter(rgx.video_id.findall(raw))

    @property
    def old_streams(self) -> Optional[VideoBulk]:
        """
        :return: channel's old livestream urls
        """
        raw = _get_old_streams(self._url)
        ids = filter(rgx.video_id.findall(raw))
        return VideoBulk(ids) if ids else None

    def uploads(self, limit: int = 20) -> Optional[VideoBulk]:
        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """
        raw = _get_uploads_data(self._url)
        videos = filter(rgx.uploads.findall(raw), limit)
        return VideoBulk(videos) if videos else None

    @property
    def latest(self) -> Optional[Video]:
        """
        :return: Channel's most recent video in Video Object form
        """
        raw = _get_uploads_data(self._url)
        any_video = rgx.video_id.findall(raw)
        return Video(any_video[0]) if any_video else None

    @property
    def subscribers(self) -> Optional[str]:
        """
        :return: total number of subscribers the channel has or None
        """
        subs = rgx.subscribers.findall(self.__raw_about)
        return subs[0] if subs else None

    @property
    def views(self) -> Optional[str]:
        """
        :return: total number of views the channel got or None
        """
        views = rgx.views.findall(self.__raw_about)
        return views[0].split(' ')[0] if views else None

    @property
    def created_at(self) -> Optional[str]:
        """
        :return: the channel creation date or None
        """
        joined_on = rgx.creation.findall(self.__raw_about)
        return joined_on[0] if joined_on else None

    @property
    def country(self) -> Optional[str]:
        """
        :return: the name of the country from where the channel is or None
        """
        country = rgx.country.findall(self.__raw_about)
        return country[0] if country else None

    @property
    def custom_url(self) -> Optional[str]:
        """
        :return: the custom _url of the channel or None
        """
        custom_urls = rgx.custom_url.findall(self.__raw_about)
        if custom_urls and '/channel/' not in custom_urls[0]:
            return custom_urls[0]

    @property
    def description(self) -> Optional[str]:
        """
        :return: the existing description of the channel
        """
        description = rgx.description.findall(self.__raw_about)
        return description[0].replace('\\n', '\n') if description else None

    @property
    def avatar(self) -> Optional[str]:
        """
        :return: logo / avatar url of the channel
        """
        av = rgx.avatar.findall(self.__raw_about)
        return av[0] if av else None

    @property
    def banner(self) -> Optional[str]:
        """
        :return: banner url of the channel
        """
        banner = rgx.banner.findall(self.__raw_about)
        return banner[0] if banner else None

    @property
    def playlists(self) -> Optional[PlaylistBulk]:
        """
        :return: a list of < playlist object > for each public playlist the channel has
        """
        raw = _get_channel_playlists(self._url)
        playlists = rgx.playlists.findall(raw)
        return PlaylistBulk(filter(playlists)) if playlists else None

    @property
    def info(self) -> Optional[Dict[str, any]]:
        """
        :return: a dict containing channel info like subscribers, views, etc.
        """

        def extract(pattern):
            data = pattern.findall(self.__raw_about)
            return data[0] if data else None

        patterns = [
            rgx.name, rgx.subscribers, rgx.views, rgx.creation,
            rgx.country, rgx.custom_url, rgx.avatar, rgx.banner, rgx.id
        ]

        data = _Thread.run(extract, patterns)

        if data[2]:
            views = data[2].split(' ')[0]
        else:
            views = None

        curl = data[5] if data[5] and '/channel/' not in data[5] else None

        return {
            'name': data[0],
            'id': data[8],
            'subscribers': data[1],
            'verified': self.verified,
            'views': views,
            'created_at': data[3],
            'country': data[4],
            'url': self._url,
            'custom_url': curl,
            'avatar': data[6],
            'banner': data[7]
        }

    @property
    def video_count(self) -> Optional[str]:
        """
        :return: the number of videos in the channel
        """
        if self.__given_id.startswith('UC'):
            q_term = self.__given_id
        else:
            q_term = self.id

        count = rgx.video_count.findall(_get_video_count(q_term))
        # handling channel with single digit video count
        return count[0].replace(',', '').replace('"', '').split()[0] if count else None

    @property
    def links(self) -> List[str]:
        """
        :return: a list of social media links added to the channel
        """
        bad_links = rgx.links.findall(self.__raw_about)
        return ['https://' + unquote(link) for link in list(set(bad_links))] if bad_links else None

    @property
    def recent_uploaded(self) -> Optional[Video]:
        raw = _get_uploads_data(self._url)
        chunk = rgx.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if not rgx.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not rgx.upload_chunk_fl_2.search(data)]
        return Video(rgx.video_id.findall(fl_2[0])[0]) if fl_2 else None

    @property
    def recent_streamed(self) -> Optional[Video]:
        raw = _get_uploads_data(self._url)
        chunk = rgx.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if rgx.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not rgx.upload_chunk_fl_2.search(data)]
        return Video(rgx.video_id.findall(fl_2[0])[0]) if fl_2 else None

    @property
    def upcoming(self) -> Optional[Upcoming]:
        raw = _get_upcoming_videos(self._url)
        if rgx.upcoming_check.search(raw):
            upcoming = rgx.upcoming.findall(raw)
            return Upcoming(upcoming[0]) if upcoming else None
        return None

    @property
    def all_upcoming(self) -> Optional[List[str]]:
        raw = _get_upcoming_videos(self._url)
        if rgx.upcoming_check.search(raw):
            video_ids = rgx.upcoming.findall(raw)
            return video_ids
        return None
