import re
from .video import Video
from .threads import _Thread
from .videobulk import _VideoBulk
from .auxiliary import _filter, _src
from .playlistbulk import _PlaylistBulk


class Channel:

    def __init__(self, channelId: str):
        """
        :param str channelId: any of channel id, url , custom url
        """
        ep = 'https://www.youtube.com/channel/'

        if '/channel/' in channelId:
            self._url = channelId
        elif '/c/' in channelId:
            self._url = channelId
        elif '/user/' in channelId:
            self._url = channelId
        else:
            self._url = ep + channelId

    def __repr__(self):
        if self.name:
            return f'<Channel - {self.name}>'
        else:
            f'<Invalid ChannelObject>'

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
        Id = re.search(r"\"channelId\":\"(.*?)\"", raw)
        if Id:
            return Id.group().replace('"', '').replace('channelId:', '')
        else:
            return

    @property
    def verified(self):
        """
        :return: bool i.e. True if channel is verified else False
        """
        raw = _src(f'{self._url}/about')
        isVerified = re.search(r'label":"Verified', raw)
        return True if isVerified else False

    @property
    def live(self):
        """
        :return: Bool of channel's Live Status
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        return '{"text":" watching"}' in raw

    @property
    def livestream(self):
        """
        :return: channel's ongoing  livestream url
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        if '{"text":" watching"}' in raw:
            Id = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))[0]
            return f'https://www.youtube.com/watch?v={Id}'

    @property
    def livestreams(self):
        """
        :return: channel's ongoing  livestream urls
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=501')
        if '{"text":" watching"}' in raw:
            Ids = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))
            return [f'https://www.youtube.com/watch?v={Id}' for Id in Ids]

    @property
    def oldstreams(self):
        """
        :return: channel's old livestream urls
        """
        raw = _src(f'{self._url}/videos?view=2&live_view=503')
        Ids = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))
        urls = [f'https://www.youtube.com/watch?v={Id}' for Id in Ids]
        return urls if urls else None

    def uploads(self, limit: int = None):
        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """
        raw = _src(f'{self._url}/videos?view=0&sort=dd&flow=grid')
        videos = _filter(re.findall(r"\"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw), limit)
        return _VideoBulk(videos) if limited else None

    @property
    def latest(self):
        """
        :return: Channel's latest uploaded video in Video Object form
        """
        raw = _src(f'{self._url}/videos?view=0&sort=dd&flow=grid')
        thumbs = re.findall('thumbnails\":\[{\"url\":\"(.*?)\?', raw)
        ups = [url for url in thumbs if '_live' not in url]
        videoId = re.findall('i/(.*?)/', ups[0])[0] if ups else None
        if videoId:
            return Video(videoId)

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
        viewList = re.findall(
            r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw
        )
        if viewList:
            return viewList[0].split(' ')[0]

    @property
    def joined(self):
        """
        :return: the channel creation date or None
        """
        raw = _src(f'{self._url}/about')
        joinList = re.findall(
            r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw
        )
        return joinList[0] if joinList else None

    @property
    def country(self):
        """
        :return: the name of the country from where the channel is or None
        """
        raw = _src(f'{self._url}/about')
        countryList = re.findall(
            r"\"country\":{\"simpleText\":\"(.*?)\"}", raw
        )
        return countryList[0] if countryList else None

    @property
    def custom_url(self):
        """
        :return: the custom _url of the channel or None
        """
        raw = _src(f'{self._url}/about')
        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        customURL = customList[0] if customList else None
        if customURL:
            if '/channel/' not in customURL:
                return customURL

    @property
    def description(self):
        """
        :return: the existing description of the channel
        """
        raw = _src(f'{self._url}/about')
        descList = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)
        return descList[0].replace('\\n', '  ') if descList else None

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
        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"", raw)
        return data[0] if data else None

    @property
    def playlists(self):
        """
        :return: a list of < playlist object > for each public playlist the channel has
        """
        raw = _src(f'{self._url}/playlists')
        idList = re.findall(r"{\"url\":\"/playlist\?list=(.*?)\"", raw)
        return _PlaylistBulk(_filter(idList)) if idList else None

    @property
    def info(self):
        """
        :return: a dict containing channel info

        dict = {
            'name': -> str,
            'id': -> str,
            'subscribers': -> str,
            'verified': -> bool,
            'total_views': -> str,
            'joined_at': -> str,
            'country': -> str,
            'url': ->str,
            'custom_url': -> str,
            'avatar_url': -> str,
            'banner_url': -> str
            }

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

        return {
            'name': ls[0],
            'id': ls[8],
            'subscribers': ls[1],
            'verified': self.verified,
            'views': views,
            'joined_at': ls[3],
            'country': ls[4],
            'url': self._url,
            'custom_url': ls[5],
            'avatar_url': ls[6],
            'banner_url': ls[7]
        }
