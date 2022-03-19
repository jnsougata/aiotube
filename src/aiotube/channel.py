from ._http import (
    get_channel_about,
    get_channel_live_data,
    get_old_streams,
    get_uploads_data,
    get_channel_playlists,
    get_video_count,
    get_upcoming_videos
)

from .live import Live
from .video import Video
from ._threads import _Thread
from urllib.parse import unquote
from .videobulk import _VideoBulk
from .auxiliary import _filter, _src
from .playlistbulk import _PlaylistBulk
from ._rgxs import _ChannelPatterns as rgx


class Channel:

    def __init__(self, channel_id: str):
        """
        :param str channel_id: any of channel id, url , custom url
        """
        head = 'https://www.youtube.com/channel/'
        if '/channel/' in channel_id:
            self._url = channel_id.replace(' ', '')
        elif '/c/' in channel_id:
            self._url = channel_id.replace(' ', '')
        elif '/user/' in channel_id:
            self._url = channel_id.replace(' ', '')
        else:
            self._url = f'{head}{channel_id}'.replace(' ', '')

    def __repr__(self):
        if self.name:
            return f'<Channel | {self.name}>'
        else:
            f'<Invalid ! ChannelObject>'

    @property
    def name(self):
        """
        :return: channel's name or None
        """
        name = rgx.name.findall(get_channel_about(self._url))
        return name[0] if name else None

    @property
    def valid(self):
        """
        :return: bool i.e. True if channel is valid else False
        """
        source = _src(self._url)
        return True if source else False

    @property
    def url(self):
        return self._url

    @property
    def id(self):
        """
        :return: the id of the channel
        """
        channel_id = rgx.id.findall(get_channel_about(self._url))
        return channel_id[0] if channel_id else None

    @property
    def verified(self):
        """
        :return: bool i.e. True if channel is verified else False
        """
        is_verified = rgx.verified.search(get_channel_about(self._url))
        return True if is_verified else False

    @property
    def live(self):
        """
        :return: channel's Live Status
        """
        check = rgx.live.findall(get_channel_live_data(self._url))
        return rgx.check_live.search(check[0]) if check else False

    @property
    def livestream(self):
        """
        :return: channel's ongoing  livestream url
        """
        raw = get_channel_live_data(self._url)
        check = rgx.live.findall(raw)
        if check and rgx.check_live.search(check[0]):
            video_id = _filter(rgx.video_id.findall(raw))[0]
            return Live(video_id)

    @property
    def livestreams(self) -> list:
        """
        :return: channel's ongoing  livestream urls
        """
        raw = get_channel_live_data(self._url)
        check = rgx.live.findall(raw)
        if check and rgx.check_live.search(check[0]):
            return _filter(rgx.video_id.findall(raw))

    @property
    def old_streams(self):
        """
        :return: channel's old livestream urls
        """
        raw = get_old_streams(self._url)
        ids = _filter(rgx.video_id.findall(raw))
        return _VideoBulk(ids)

    def uploads(self, limit: int = 10):
        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """
        raw = get_uploads_data(self._url)
        videos = _filter(rgx.uploads.findall(raw), limit)
        return _VideoBulk(videos) if videos else None

    @property
    def latest(self):
        """
        :return: Channel's most recent video in Video Object form
        """
        raw = get_uploads_data(self._url)
        any_video = rgx.video_id.findall(raw)
        return Video(any_video[0]) if any_video else None

    @property
    def subscribers(self):
        """
        :return: total number of subscribers the channel has or None
        """
        raw = get_channel_about(self._url)
        subs = rgx.subscribers.findall(raw)
        return subs[0] if subs else None

    @property
    def views(self):
        """
        :return: total number of views the channel got or None
        """
        raw = get_channel_about(self._url)
        views = rgx.views.findall(raw)
        return views[0].split(' ')[0] if views else None

    @property
    def created_at(self):
        """
        :return: the channel creation date or None
        """
        raw = get_channel_about(self._url)
        joined_on = rgx.creation.findall(raw)
        return joined_on[0] if joined_on else None

    @property
    def country(self):
        """
        :return: the name of the country from where the channel is or None
        """
        raw = get_channel_about(self._url)
        country = rgx.country.findall(raw)
        return country[0] if country else None

    @property
    def custom_url(self):
        """
        :return: the custom _url of the channel or None
        """
        raw = get_channel_about(self._url)
        custom_urls = rgx.custom_url.findall(raw)
        if custom_urls and '/channel/' not in custom_urls[0]:
            return custom_urls[0]

    @property
    def description(self):
        """
        :return: the existing description of the channel
        """
        raw = get_channel_about(self._url)
        description = rgx.description.findall(raw)
        return description[0].replace('\\n', '\n') if description else None

    @property
    def avatar(self):
        """
        :return: logo / avatar url of the channel
        """
        raw = get_channel_about(self._url)
        av = rgx.avatar.findall(raw)
        return av[0] if av else None

    @property
    def banner(self):
        """
        :return: banner url of the channel
        """
        raw = get_channel_about(self._url)
        banner = rgx.banner.findall(raw)
        return banner[0] if banner else None

    @property
    def playlists(self):
        """
        :return: a list of < playlist object > for each public playlist the channel has
        """
        raw = get_channel_playlists(self._url)
        playlists = rgx.playlists.findall(raw)
        return _PlaylistBulk(_filter(playlists)) if playlists else None

    @property
    def info(self):
        """
        :return: a dict containing channel info like subscribers, views, etc.
        """
        raw = get_channel_about(self._url)

        def extract(pattern):
            data = pattern.findall(raw)
            return data[0] if data else None

        patterns = [rgx.name, rgx.subscribers, rgx.views, rgx.creation,
                    rgx.country, rgx.custom_url, rgx.avatar, rgx.banner, rgx.id]

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
            'avatar_url': data[6],
            'banner_url': data[7]
        }

    @property
    def video_count(self):
        """
        :return: the number of videos in the channel
        """
        # TODO: reduce the number of requests to 1
        raw = get_video_count(self.id)
        counts = rgx.video_count.findall(raw)
        # handling channel with single digit video count
        return counts[0].replace(',', '').replace('"', '').split()[0] if counts else None

    @property
    def links(self) -> list:
        """
        :return: a list of social media links added to the channel
        """
        raw = get_channel_about(self._url)
        bad_links = rgx.links.findall(raw)
        return ['https://' + unquote(link) for link in list(set(bad_links))] if bad_links else None

    @property
    def recent_uploaded(self):
        raw = get_uploads_data(self._url)
        chunk = rgx.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if not rgx.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not rgx.upload_chunk_fl_2.search(data)]
        return Video(rgx.video_id.findall(fl_2[0])[0]) if fl_2 else None

    @property
    def recent_streamed(self):
        raw = get_uploads_data(self._url)
        chunk = rgx.upload_chunk.findall(raw)
        fl_1 = [data for data in chunk if rgx.upload_chunk_fl_1.search(data)]
        fl_2 = [data for data in fl_1 if not rgx.upload_chunk_fl_2.search(data)]
        return Video(rgx.video_id.findall(fl_2[0])[0]) if fl_2 else None

    @property
    def upcoming(self):
        raw = get_upcoming_videos(self._url)
        if rgx.upcoming_check.search(raw):
            upcoming = rgx.upcoming.findall(raw)
            return Video(upcoming[0]) if upcoming else None
        return None

    @property
    def all_upcoming(self):
        raw = get_upcoming_videos(self._url)
        if rgx.upcoming_check.search(raw):
            video_ids = rgx.upcoming.findall(raw)
            return video_ids
        return None
