import re
import urllib.request
from .__vid__ import Video
from .__proc__ import _filter
from .__hyp__ import _HyperThread
from urllib.error import HTTPError
from .__vidbulk__ import _VideoBulk
from .__pllsbulk__ import _PlaylistBulk



class Channel:

    def __init__(self, channelId:str):

        """
        :param str channelId: any of channel _id, _url , custom _url
        """

        if '/channel/' in channelId:
            self._url = channelId

        elif '/c/' in channelId:
            self._url = channelId

        elif '/user/' in channelId:
            self._url = channelId
        else:
            def check(part: str) -> str or None:
                url = f'{part}{channelId}'
                try:
                    urllib.request.urlopen(url)
                    return url
                except HTTPError:
                    return None

            ls = _HyperThread.run(
                check,
                [
                    'https://youtube.com/channel/',
                    'https://youtube.com/c/'
                ]

            )
            ls.remove(None)

            self._url = ls[0] if len(ls) > 0 else None


    @property
    def url(self):
        return self._url


    @property
    def id(self):

        """
        :return: the ID of the channel
        """

        raw = urllib.request.urlopen(f'{self._url}/about').read().decode()
        Id = re.search(r"\"channelId\":\"(.*?)\"", raw)
        return Id.group().replace('"','').replace('channelId:','') if Id else None


    @property
    def verified(self):
        raw = urllib.request.urlopen(self._url).read().decode()
        isVerified = re.search(r'label":"Verified', raw)
        return True if isVerified else False


    @property
    def live(self):

        """
        :return: Bool of channel is Live Status
        """

        raw = urllib.request.urlopen(self._url).read().decode()
        isLive = re.search(r'{"text":" watching"}', raw)
        return True if isLive else False


    @property
    def stream_link(self):

        """
        :return: channel's ongoing  livestream _url
        """

        raw = urllib.request.urlopen(self._url).read().decode()

        isLive = re.search(r'{"text":" watching"}', raw)

        if isLive:
            Id = re.search(r"watch\?v=(.*?)\"", raw).group().replace('watch?v=','').replace('"','')
            return f'https://www.youtube.com/watch?v={Id}'
        else:
            return None


    def uploads(self, limit:int = None):

        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """

        QUERY = f'{self._url}/videos?view=0&sort=dd&flow=grid'
        raw = urllib.request.urlopen(QUERY).read().decode()
        videos = re.findall(r"\"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw)
        limited = videos[:(limit - len(videos))] if limit is not None and limit < 30 else videos
        return _VideoBulk(limited) if len(limited) > 0 else None


    @property
    def latest(self):
        """
        :return: Channel's latest uploaded video in Video Object form
        """
        QUERY = f'{self._url}/videos?view=0&sort=dd&flow=grid'
        raw = urllib.request.urlopen(QUERY).read().decode()
        videos = re.findall(r"\[{\"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw)
        return Video(videos[0]) if len(videos) > 0 else None


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

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()

        def get_data(pattern):
            data = re.findall(pattern, raw)
            return data[0] if len(data) > 0 else None

        patterns = [

            r"channelMetadataRenderer\":{\"title\":\"(.*?)\"",
            r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\"",
            r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}",
            r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}",
            r"\"country\":{\"simpleText\":\"(.*?)\"}",
            r"\"canonicalChannelUrl\":\"(.*?)\"",
            "height\":88},{\"url\":\"(.*?)\"",
            r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"",
            r"channelId\":\"(.*?)\""

        ]

        ls = _HyperThread.run(get_data, patterns)

        infoDict = {
            'name': ls[0],
            'id': ls[8],
            'subscribers': ls[1][:-12],
            'verified':self.verified,
            'total_views': ls[2][:-6],
            'joined_at': ls[3],
            'country': ls[4],
            'url': self._url,
            'custom_url': ls[5],
            'avatar_url': ls[6],
            'banner_url': ls[7]
        }

        return infoDict


    @property
    def name(self):

        """
        :return: name of the channel or None
        """

        name_raw = urllib.request.urlopen(f'{self._url}/about').read().decode()
        titleList = re.findall(r"channelMetadataRenderer\":{\"title\":\"(.*?)\"", name_raw)
        return titleList[0] if len(titleList) > 0 else None


    @property
    def subscribers(self):

        """
        :return: total number of subscribers the channel has or None
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        subList = re.findall(
            r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\"",raw
        )
        return subList[0][:-12] if len(subList) != 0 else None


    @property
    def total_views(self):

        """
        :return: total number of views the channel got or None
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        totViewList = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw)
        return totViewList[0][:-6] if len(totViewList) != 0 else None


    @property
    def joined(self):

        """
        :return: the channel creation date or None
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        joinList = re.findall(r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw)
        return joinList[0] if len(joinList) != 0 else None


    @property
    def country(self):

        """
        :return: the name of the country from where the channel is or None
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        countryList = re.findall(r"\"country\":{\"simpleText\":\"(.*?)\"}", raw)
        return countryList[0] if len(countryList) != 0 else None


    @property
    def custom_url(self):

        """
        :return: the custom _url of the channel or None
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        customURL = customList[0] if len(customList) != 0 else None
        return customURL if '/channel/' not in customURL and customURL is not None else None


    @property
    def description(self):

        """
        :return: the existing description of the channel
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        descList = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)
        return descList[0].replace('\\n', '') if len(descList) > 0 else None


    @property
    def avatar_url(self):

        """
        :return: logo / avatar url of the channel
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall("height\":88},{\"url\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def banner_url(self):

        """
        :return: banner url of the channel
        """

        QUERY = f'{self._url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def playlists(self):

        """
        :return: a list of < playlist object > for each public playlist the channel has
        """

        url = f'{self._url}/playlists'
        raw = urllib.request.urlopen(url).read().decode()
        idList = re.findall(r"{\"url\":\"/playlist\?list=(.*?)\"", raw)
        return _PlaylistBulk(_filter(idList)) if len(idList) > 0 else None
