import re
import urllib.request


def Purify(limit:int, iterable:list):
    pure = list(set(iterable))
    if limit is None:
        return pure
    else:
        num = int(len(pure) - limit)
        try:
            return pure[:-num]
        except IndexError:
            return pure



class Channel:

    def __init__(self,ChanneLid:str):

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
        raw = urllib.request.urlopen(self.url).read().decode()
        idList = re.findall(r"channelId\":\"(.*?)\"",raw)

        return idList[0] if len(idList) != 0 else None


    @property
    def live(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        isLive = re.findall(r"\"text\":\" (\S{8})", raw)

        return True if len(isLive) != 0 and isLive[0] == 'watching' else False


    @property
    def stream_link(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        if self.live:
            VideoIDList = re.findall(r"watch\?v=(\S{11})", raw)
            return f'https://www.youtube.com/watch?v={VideoIDList[0]}'
        else:
            return None


    def latest_uploads(self, limit:int = None):
        QUERY = f'{self.url}/videos'
        raw = urllib.request.urlopen(QUERY).read().decode()

        VideoIDList = re.findall(r"watch\?v=(\S{11})", raw)
        pureList = Purify(limit=limit, iterable=VideoIDList)

        return [Video(item) for item in pureList]


    @property
    def info(self):
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
            'joined_at':joinDate,
            'country':country,
            'url':self.url,
            'custom_url':customURl,
            'avatar_url':avatar,
            'banner_url':banner}

        return aboutDict


    @property
    def name(self):
        name_raw = urllib.request.urlopen(f'{self.url}/about').read().decode()
        titleList = re.findall(r"channelMetadataRenderer\":{\"title\":\"(.*?)\"", name_raw)

        return titleList[0] if len(titleList) != 0 else None


    @property
    def subs(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        subList = re.findall(
            r"\"subscriberCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?)\"",raw
        )

        return subList[0][:-12] if len(subList) != 0 else None


    @property
    def total_views(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        totViewList = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"}", raw)

        return totViewList[0][:-6] if len(totViewList) != 0 else None


    @property
    def joined_at(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        joinList = re.findall(r"{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}", raw)

        return joinList[0] if len(joinList) != 0 else None


    @property
    def country(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        countryList = re.findall(r"\"country\":{\"simpleText\":\"(.*?)\"}", raw)

        return countryList[0] if len(countryList) != 0 else None


    @property
    def custom_url(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        customList = re.findall(r"\"canonicalChannelUrl\":\"(.*?)\"", raw)

        customURL = customList[0] if len(customList) != 0 else None

        return customURL if '/channel/' not in customURL else None


    @property
    def description(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        descList = re.findall(r"{\"description\":{\"simpleText\":\"(.*?)\"}", raw)

        return descList[0] if len(descList) != 0 else None


    @property
    def avatar_url(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall("height\":88},{\"url\":\"(.*?)\"",raw)

        return data[0] if len(data) != 0 else None


    @property
    def banner_url(self):
        QUERY = f'{self.url}/about'
        raw = urllib.request.urlopen(QUERY).read().decode()
        data = re.findall(r"width\":1280,\"height\":351},{\"url\":\"(.*?)\"",raw)

        return data[0] if len(data) != 0 else None


    @property
    def playlists(self):
        url = f'{self.url}/playlists'
        raw = urllib.request.urlopen(url).read().decode()
        idList = re.findall(r"{\"url\":\"/playlist\?list=(.*?)\"", raw)

        return [Playlist(item) for item in list(set(idList))]



class Playlist:
    def __init__(self, playlist_id:str):
        self.id = playlist_id

    @property
    def info(self):
        try:
            url = f'https://www.youtube.com/playlist?list={self.id}'
            raw = urllib.request.urlopen(url).read().decode()

            name_data = re.findall(r"{\"title\":\"(.*?)\"",raw)

            video_count = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"",raw)

            thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)

            videos = list(set(re.findall(r"videoId\":\"(.*?)\"", raw)))

            data_dict = {
                'name': name_data[0] if len(name_data) != 0 else None,
                'url': url,
                'video_count':video_count[0] if len(video_count) != 0 else None,
                'videos': videos,
                'thumbnail':thumbnails[0] if len(thumbnails) != 0 else None,
            }

            return data_dict

        except:
            return None


    @property
    def name(self):
        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()

        name_data = re.findall(r"{\"title\":\"(.*?)\"", raw)

        return name_data[0] if len(name_data) != 0 else None


    @property
    def url(self):
        url = f'https://www.youtube.com/playlist?list={self.id}'

        return url


    @property
    def video_count(self):
        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()

        video_count = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"", raw)

        return video_count[0] if len(video_count) != 0 else None


    def videos(self, limit:int = None):
        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()

        videos = list(set(re.findall(r"videoId\":\"(.*?)\"", raw)))

        pure = Purify(limit=limit, iterable=videos)

        return [Video(item) for item in pure]

    @property
    def thumbnail(self):
        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()

        thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)

        return thumbnails[0] if len(thumbnails) != 0 else None



class Video:

    def __init__(self, videoId:str):
        if len(videoId) > 15:

            if 'watch?v=' in videoId:
                self.url = videoId
                self.id = re.findall(r"v=(.*)", videoId)[0]

            elif 'youtu.be/' in videoId:
                idL = re.findall(r"youtu\.be/(.*)", videoId)
                self.url = f'https://www.youtube.com/watch?v={idL[0]}'
                self.id = re.findall(r"/(.*)", videoId)[0]
        else:
            self.url = f'https://www.youtube.com/watch?v={videoId}'
            self.id = videoId


    @property
    def title(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"title\":\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None


    @property
    def views(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"", raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def likes(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"label\":\"(.*?) likes\"", raw)
        return data[0] if len(data) != 0 else None


    @property
    def dislikes(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def duration(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"approxDurationMs\":\"(.*?)\"",raw)
        return f'{data[0]}ms' if len(data) != 0 else None


    @property
    def upload_date(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"uploadDate\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def channel_id(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"channelIds\":\[\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def description(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable",raw)
        return data[0] if len(data) != 0 else None


    @property
    def thumbnail(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def tags(self):
        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">",raw)
        return data[0].split(',') if len(data) != 0 else None


    @property
    def info(self):
        raw = urllib.request.urlopen(self.url).read().decode()

        title_data = re.findall(r"\"title\":\"(.*?)\"", raw)

        v_data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"", raw
        )
        views_data = v_data[0] if len(v_data) != 0 else None

        likes_data_list = re.findall(r"\"label\":\"(.*?) likes\"", raw)
        likes_data = likes_data_list[0] if len(likes_data_list) != 0 else None

        dislikes_data_list = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )
        dislikes_data = dislikes_data_list[0] if len(dislikes_data_list) != 0 else None

        duration_data_list = re.findall(r"approxDurationMs\":\"(.*?)\"", raw)
        duration_data = duration_data_list[0] if len(duration_data_list) != 0 else None

        date_data_list = re.findall(r"uploadDate\":\"(.*?)\"", raw)
        date_data = date_data_list[0] if len(date_data_list) != 0 else None

        id_data_list = re.findall(r"channelIds\":\[\"(.*?)\"", raw)
        id_data = id_data_list[0] if len(id_data_list) != 0 else None

        desc_data_list = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable", raw)
        desc_data = desc_data_list[0] if len(desc_data_list) != 0 else None

        thumb_data_list = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        thumb_data = thumb_data_list[0] if len(thumb_data_list) != 0 else None

        tags_data_list = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)
        tags = tags_data_list[0].split(',') if len(tags_data_list) != 0 else None

        infoDict = {
            'title':title_data,
            'id':self.id,
            'views':views_data,
            'likes':likes_data,
            'dislikes':dislikes_data,
            'channel_id':id_data,
            'duration':duration_data,
            'upload_date':date_data,
            'thumbnail':thumb_data,
            'tags':tags,
            'url':self.url,
            'description': desc_data
        }
        return infoDict

    

class Search:

    def __init__(self,keyword:str):
        query = keyword.replace(" ", '+')
        self.parser = query


    @property
    def get_video(self):
        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        video_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        return Video(video_ids[0]) if len(video_ids) != 0 else None


    @property
    def get_channel(self):
        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        channel_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        return Channel(channel_ids[0]) if len(channel_ids) != 0 else None


    def get_videos(self, limit: int = None):
        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        pureList = Purify(limit=limit, iterable=raw_ids)
        return [Video(item) for item in pureList] if len(pureList) != 0 else None


    def get_channels(self,limit:int = None):
        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        pureList = Purify(limit=limit, iterable=raw_ids)
        return [Channel(item) for item in pureList] if len(pureList) != 0 else None


    @property
    def get_playlist(self):
        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAw%253D%253D'
        raw = urllib.request.urlopen(url=url).read().decode()
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        return Playlist(found[0]) if len(found) != 0 else None



class Extras:

    def __init__(self):
        pass

    @property
    def Trending(self):
        url = f'https://www.youtube.com/feed/trending'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return Video(data[0]) if len(data) != 0 else None


    @property
    def Music(self):
        url = f'https://www.youtube.com/feed/music'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None


    @property
    def Gaming(self):
        url = f'https://www.youtube.com/gaming'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def News(self):
        url = f'https://www.youtube.com/news'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def Live(self):
        url = f'https://www.youtube.com/live'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def Learning(self):
        url = f'https://www.youtube.com/learning'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None


    @property
    def Sports(self):
        url = f'https://www.youtube.com/sports'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None
