import re
from .live import Live
from .video import Video
from ._threads import _Thread
from urllib.parse import unquote
from .videobulk import _VideoBulk
from .auxiliary import _filter, _src
from .playlistbulk import _PlaylistBulk


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
        raw = _src(f'{self._url}/about')
        name = re.findall("channelMetadataRenderer\":{\"title\":\"(.*?)\"", raw)
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
        raw = _src(f'{self._url}/about')
        _id = re.search(r"\"channelId\":\"(.*?)\"", raw)
        if _id:
            return _id.group().replace('"', '').replace('channelId:', '')

    @property
    def verified(self):
        """
        :return: bool i.e. True if channel is verified else False
        """
        raw = _src(f'{self._url}/about')
        is_verified = re.search(r'label":"Verified', raw)
        return True if is_verified else False

    @property
    def live(self):
        """
        :return: Bool of channel's Live Status
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        check = re.findall("thumbnailOverlays\":\[(.*?)]", raw)
        return '{"text":"LIVE"}' in check[0] if check else False

    @property
    def livestream(self):
        """
        :return: channel's ongoing  livestream url
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        check = re.findall("thumbnailOverlays\":\[(.*?)]", raw)
        if check and '{"text":"LIVE"}' in check[0]:
            id_ = _filter(re.findall(r"videoId\":\"(.*?)\"", raw))[0]
            return Live(id_)

    @property
    def livestreams(self) -> list:
        """
        :return: channel's ongoing  livestream urls
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        if '{"text":" watching"}' in raw:
            ids = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))
            return [Live(id_) for id_ in ids]

    @property
    def old_streams(self):
        """
        :return: channel's old livestream urls
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=503')
        ids = _filter(re.findall(r"videoId\":\"(.*?)\"", raw))
        return _VideoBulk(ids)

    def uploads(self, limit: int = None):
        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """
        raw = _src(f'{self._url}/videos?view=0&sort=dd&flow=grid')
        videos = _filter(re.findall(r"\"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw), limit)
        return _VideoBulk(videos) if videos else None

    @property
    def latest(self):
        """
        :return: Channel's latest uploaded video in Video Object form
        """
        raw = _src(f'{self._url}/videos?view=0&sort=dd&flow=grid')
        thumbs = re.findall('thumbnails\":\[{\"url\":\"(.*?)\?', raw)
        ups = [url for url in thumbs if '_live' not in url]
        video_id = re.findall('i/(.*?)/', ups[0]) if ups else None
        return Video(video_id[0]) if video_id else None

    @property
    def subscribers(self):
        """
        :return: total number of subscribers the channel has or None
        """
        raw = _src(f'{self._url}/about')
        subs = re.findall("}},\"simpleText\":\"(.*?) ", raw)
        return subs[0] if subs else None

    @property
    def views(self):
        """
        :return: total number of views the channel got or None
        """
        raw = _src(f'{self._url}/about')
        view_list = re.findall(
            r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw
        )
        if view_list:
            return view_list[0].split(' ')[0]

    @property
    def created_at(self):
        """
        :return: the channel creation date or None
        """
        raw = _src(f'{self._url}/about')
        join_list = re.findall(
            r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw
        )
        return join_list[0] if join_list else None

    @property
    def country(self):
        """
        :return: the name of the country from where the channel is or None
        """
        raw = _src(f'{self._url}/about')
        country_list = re.findall(
            r"\"country\":{\"simpleText\":\"(.*?)\"}", raw
        )
        return country_list[0] if country_list else None

    @property
    def custom_url(self):
        """
        :return: the custom _url of the channel or None
        """
        raw = _src(f'{self._url}/about')
        custom_list = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        custom_url = custom_list[0] if custom_list else None
        if custom_url:
            if '/channel/' not in custom_url:
                return custom_url

    @property
    def description(self):
        """
        :return: the existing description of the channel
        """
        raw = _src(f'{self._url}/about')
        desc_list = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)
        return desc_list[0].replace('\\n', '  ') if desc_list else None

    @property
    def avatar(self):
        """
        :return: logo / avatar url of the channel
        """
        raw = _src(f'{self._url}/about')
        data = re.findall("height\":88},{\"url\":\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def banner(self):
        """
        :return: banner url of the channel
        """
        raw = _src(f'{self._url}/about')
        data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def playlists(self):
        """
        :return: a list of < playlist object > for each public playlist the channel has
        """
        raw = _src(f'{self._url}/playlists')
        id_list = re.findall(r"{\"url\":\"/playlist\?list=(.*?)\"", raw)
        return _PlaylistBulk(_filter(id_list)) if id_list else None

    @property
    def info(self):
        """
        :return: a dict containing channel info like subscribers, views, etc.
        """
        raw = _src(f'{self._url}/about')

        def extract(pattern):
            data = re.findall(pattern, raw)
            return data[0] if data else None

        patterns = [

            "channelMetadataRenderer\":{\"title\":\"(.*?)\"",
            "}},\"simpleText\":\"(.*?) ",
            "\"viewCountText\":{\"simpleText\":\"(.*?)\"}",
            "{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}",
            "\"country\":{\"simpleText\":\"(.*?)\"}",
            "\"canonicalChannelUrl\":\"(.*?)\"",
            "height\":88},{\"url\":\"(.*?)\"",
            "width\":1280,\"height\":351},{\"url\":\"(.*?)\"",
            "channelId\":\"(.*?)\""

        ]

        ls = _Thread.run(extract, patterns)

        if ls[2]:
            views = ls[2].split(' ')[0]
        else:
            views = None

        curl = ls[5] if ls[5] and '/channel' not in ls[5] else None

        return {
            'name': ls[0],
            'id': ls[8],
            'subscribers': ls[1],
            'verified': self.verified,
            'views': views,
            'created_at': ls[3],
            'country': ls[4],
            'url': self._url,
            'custom_url': curl,
            'avatar_url': ls[6],
            'banner_url': ls[7]
        }

    @property
    def video_count(self):
        """
        :return: the number of videos in the channel
        """
        # TODO: reduce the number of requests to 1
        raw = _src(f'https://www.youtube.com/results?search_query={self.id}&sp=EgIQAg%253D%253D')
        counts = re.findall('videoCountText\":{\"runs\":\[{\"text\":(.*?)}', raw)
        print(counts)
        count_string = counts[0].replace(',', '').replace('"', '') if counts else None
        # handling channel with single digit video count
        if count_string:
            return int(count_string.split()[0])

    @property
    def links(self) -> list:
        """
        :return: a list of social media links added to the channel
        """
        raw = _src(f'{self._url}/about')
        bad_links = re.findall('q=https%3A%2F%2F(.*?)"', raw)
        filtered = ['https://' + unquote(link) for link in list(set(bad_links))]
        return filtered if filtered else None
