import re
import urllib.request
from .__vid__ import Video
from .__plls__ import Playlist
from .__proc__ import _filter

class Channel:

    def __init__(self,ChanneLid:str):

        """

        :param str ChanneLid: any of channel id, url , custom url

        """

        if len(ChanneLid) < 30:
            try:
                url = f'https://www.youtube.com/channel/{ChanneLid}'
                urllib.request.urlopen(url)
                self.url = url
            except:
                url = f'https://www.youtube.com/c/{ChanneLid}'
                try:
                    urllib.request.urlopen(url)
                    self.url = url
                except:
                    print('Invalid Channel URL or ID')
                    self.url = None
        else:
            if '/channel/' in ChanneLid:
                self.url = ChanneLid

            elif '/c/' in ChanneLid:
                self.url = ChanneLid


    @property
    def id(self):

        """

        :return: the ID of the channel

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        idList = re.findall(r"channelId\":\"(.*?)\"",raw)
        return idList[0] if len(idList) != 0 else None


    @property
    def live(self):

        """

        :return: Bool of channel is Live Status

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        isLive = re.findall(r"\"text\":\" (\S{8})", raw)
        return True if len(isLive) != 0 and isLive[0] == 'watching' else False


    @property
    def stream_link(self):

        """

        :return: channel's ongoing  livestream url

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        videoIdList = re.findall(r"watch\?v=(\S{11})", raw)
        return f'https://www.youtube.com/watch?v={videoIdList[0]}' if self.live and len(videoIdList) != 0 else None



    def latest_uploads(self, limit:int = None):

        """

        :param int limit: number of videos user wants from channel's latest upload
        :return: a list of < video objects > for each latest uploaded video (consider limit)

        """

        QUERY = f'{self.url}/videos'
        raw = urllib.request.urlopen(QUERY).read().decode()
        VideoIDList = re.findall(r"watch\?v=(\S{11})", raw)
        pureList = _filter(limit=limit, iterable=VideoIDList)
        return [Video(item) for item in pureList]


    @property
    def info(self):

        """

        :return: a dict containing channel info

        dict = {
            'name':name,
            'id':id,
            'subscribers':subs,
            'total_views': totalView,
            'joined_at':joinDate,
            'country':country,
            'url':self.url,
            'custom_url':customURl,
            'avatar_url':avatar,
            'banner_url':banner
            }

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()

        titleList = re.findall(r"channelMetadataRenderer\":{\"title\":\"(.*?)\"", raw)
        name = titleList[0] if len(titleList) != 0 else None

        subList = re.findall(r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\"",raw)
        subs = subList[0][:-12] if len(subList) != 0 else None

        totViewList = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw)
        totalView = totViewList[0][:-6] if len(totViewList) != 0 else None

        joinList = re.findall(r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw)
        joinDate = joinList[0] if len(joinList) != 0 else None

        countryList = re.findall(r"\"country\":{\"simpleText\":\"(.*?)\"}", raw)
        country = countryList[0] if len(countryList) != 0 else None

        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        is_customURL = customList[0] if len(customList) != 0 else None
        customURl = is_customURL if is_customURL is not None and '/channel/' not in is_customURL else None

        avatar_data = re.findall("height\":88},{\"url\":\"(.*?)\"", raw)
        avatar = avatar_data[0] if len(avatar_data) != 0 else None

        banner_data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"", raw)
        banner = banner_data[0] if len(banner_data) != 0 else None

        channelIds = re.findall(r"channelId\":\"(.*?)\"",raw)
        id = channelIds[0] if len(channelIds) != 0 else None

        aboutDict = {

            'name':name,
            'id':id,
            'subscribers':subs,
            'total_views': totalView,
            'joined':joinDate,
            'country':country,
            'url':self.url,
            'custom_url':customURl,
            'avatar_url':avatar,
            'banner_url':banner
        }

        return aboutDict


    @property
    def name(self):

        """

        :return: name of the channel or None

        """

        name_raw = urllib.request.urlopen(f'{self.url}/about').read().decode()
        titleList = re.findall(r"channelMetadataRenderer\":{\"title\":\"(.*?)\"", name_raw)
        return titleList[0] if len(titleList) != 0 else None


    @property
    def subscribers(self):

        """

        :return: total number of subscribers the channel has or None

        """

        QUERY = f'{self.url}/about'
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

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        totViewList = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw)
        return totViewList[0][:-6] if len(totViewList) != 0 else None


    @property
    def joined(self):

        """

        :return: the channel creation date or None

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        joinList = re.findall(r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw)
        return joinList[0] if len(joinList) != 0 else None


    @property
    def country(self):

        """

        :return: the name of the country from where the channel is or None

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        countryList = re.findall(r"\"country\":{\"simpleText\":\"(.*?)\"}", raw)
        return countryList[0] if len(countryList) != 0 else None


    @property
    def custom_url(self):

        """

        :return: the custom url of the channel or None

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        customURL = customList[0] if len(customList) != 0 else None
        return customURL if '/channel/' not in customURL and customURL is not None else None


    @property
    def description(self):

        """

        :return: the existing description of the channel

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        descList = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)
        return descList[0] if len(descList) != 0 else None


    @property
    def avatar_url(self):

        """

        :return: logo url of the channel

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall("height\":88},{\"url\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def banner_url(self):

        """

        :return: banner url of the channel

        """

        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def playlists(self):

        """

        :return: a list if < playlist object > for each public playlist the channel has

        """

        url = f'{self.url}/playlists'
        raw = urllib.request.urlopen(url).read().decode()
        idList = re.findall(r"{\"url\":\"/playlist\?list=(.*?)\"", raw)
        return [Playlist(item) for item in _filter(idList)]