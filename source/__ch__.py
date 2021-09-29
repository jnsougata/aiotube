import re
import json
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
            self._url = f'https://www.youtube.com/channel/{channelId}'



    def __repr__(self):
        _name = self.name
        return _name if _name is not None else 'invalid'


    @property
    def valid(self):
        _url = self._url
        try:
            urllib.request.urlopen(_url)
            return True
        except HTTPError as e:
            if e.code == 404:
                return False
            elif e.code == 429:
                return None


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

        """
        :return: bool i.e. True if channel is verified else False
        """

        raw = urllib.request.urlopen(f'{self._url}/about').read().decode()
        isVerified = re.search(r'label":"Verified', raw)
        return True if isVerified else False


    @property
    def live(self):

        """
        :return: Bool of channel's Live Status
        """

        raw = urllib.request.urlopen(f'{self._url}/videos?view=2&live_view=501').read().decode()
        return '{"text":" watching"}' in raw



    @property
    def streaming_now(self):

        """
        :return: channel's ongoing  livestream url
        """

        raw = urllib.request.urlopen(f'{self._url}/videos?view=2&live_view=501').read().decode()

        if '{"text":" watching"}' in raw:
            Id = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))[0]
            return f'https://www.youtube.com/watch?v={Id}'



    @property
    def streaming_all_now(self):

        """
        :return: channel's ongoing  livestream urls
        """

        raw = urllib.request.urlopen(
            f'{self._url}/videos?view=2&live_view=501'
        ).read().decode()

        if '{"text":" watching"}' in raw:
            Ids = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))
            return [f'https://www.youtube.com/watch?v={Id}' for Id in Ids]



    @property
    def past_streams(self):

        """
        :return: channel's old livestream urls
        """

        raw = urllib.request.urlopen(
            f'{self._url}/videos?view=2&live_view=503'
        ).read().decode()

        Ids = _filter(re.findall(r"\"videoId\":\"(.*?)\"", raw))
        urls = [f'https://www.youtube.com/watch?v={Id}' for Id in Ids]
        return urls if len(urls) > 0 else None



    def uploads(self, limit:int = None):

        """
        :param int limit: number of videos user wants from channel's latest upload
        :return: a < bulk video obj > of latest uploaded videos (consider limit)
        """

        query = f'{self._url}/videos?view=0&sort=dd&flow=grid'
        raw = urllib.request.urlopen(query).read().decode()
        videos = re.findall(r"\"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw)
        limited = videos[:(limit - len(videos))] if limit is not None and limit < 30 else videos
        return _VideoBulk(limited) if len(limited) > 0 else None



    @property
    def latest(self):

        """
        :return: Channel's latest uploaded video in Video Object form
        """
        def check(Id):
            if 'live' not in Video(Id).thumbnail:
                return Id
            else:
                return None

        query = f'{self._url}/videos?view=0&sort=dd&flow=grid'
        raw = urllib.request.urlopen(query).read().decode()
        videos = re.findall(r"gridVideoRenderer\":{\"videoId\":\"(.*?)\"", raw)
        if len(videos) > 0:
            if '_live' not in raw:
                return Video(videos[0])
            else:
                ls = _HyperThread.run(check,videos)
                true_type = [Id for Id in ls if Id is not None]
                return Video(true_type[0]) if len(true_type) > 0 else None



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

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()

        def get_data(pattern):
            data = re.findall(pattern, raw)
            return data[0] if len(data) > 0 else None

        patterns = [

            "channelMetadataRenderer\":{\"title\":\"(.*?)\"",
            "subscriberCountText\":(.*?)B",
            "\"viewCountText\":{\"simpleText\":\"(.*?)\"}",
            "{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}",
            "\"country\":{\"simpleText\":\"(.*?)\"}",
            "\"canonicalChannelUrl\":\"(.*?)\"",
            "height\":88},{\"url\":\"(.*?)\"",
            "width\":1280,\"height\":351},{\"url\":\"(.*?)\"",
            "channelId\":\"(.*?)\""

        ]

        ls = _HyperThread.run(get_data, patterns)
        
        if len(ls[1]) > 0:
            strJSON = ls[1][0].replace(',"tv', '')
            dct = json.loads(strJSON)
            sub = dct['simpleText'].split(' ')[0]
        else:
            sub = None
            
        if len(ls[2]) > 0:
            views = ls[2].split(' ')[0]
        else:
            views = None

        infoDict = {
            'name': ls[0],
            'id': ls[8],
            'subscribers': sub,
            'verified':self.verified,
            'total_views': views,
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

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        dict_raw = re.findall("\"subscriberCountText\":(.*?)B", raw)
        if len(dict_raw) > 0:
            strJSON = dict_raw[0].replace(',"tv', '')
            final_dict = json.loads(strJSON)
            return final_dict['simpleText'].split(' ')[0]


    @property
    def total_views(self):

        """
        :return: total number of views the channel got or None
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        viewList = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw)
        if len(viewList) > 0:
            final = viewList[0].split(' ')
            return final[0]


    @property
    def joined(self):

        """
        :return: the channel creation date or None
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        joinList = re.findall(r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw)
        return joinList[0] if len(joinList) != 0 else None


    @property
    def country(self):

        """
        :return: the name of the country from where the channel is or None
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        countryList = re.findall(r"\"country\":{\"simpleText\":\"(.*?)\"}", raw)
        return countryList[0] if len(countryList) > 0 else None


    @property
    def custom_url(self):

        """
        :return: the custom _url of the channel or None
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)
        customURL = customList[0] if len(customList) != 0 else None
        return customURL if '/channel/' not in customURL and customURL is not None else None


    @property
    def description(self):

        """
        :return: the existing description of the channel
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        descList = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)
        return descList[0].replace('\\n', '  ') if len(descList) > 0 else None


    @property
    def avatar_url(self):

        """
        :return: logo / avatar url of the channel
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
        data = re.findall("height\":88},{\"url\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def banner_url(self):

        """
        :return: banner url of the channel
        """

        query = f'{self._url}/about'
        raw = urllib.request.urlopen(query).read().decode()
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
