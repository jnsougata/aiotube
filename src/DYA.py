"""
MIT License

Copyright (c) 2021 Zen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""




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
        pureList = Purify(limit=limit, iterable=VideoIDList)
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
            'joined_at':joinDate,
            'country':country,
            'url':self.url,
            'custom_url':customURl,
            'avatar_url':avatar,
            'banner_url':banner}

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
    def subs(self):
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
    def joined_at(self):
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
        return [Playlist(item) for item in list(set(idList))]



class Playlist:
    def __init__(self, playlist_id:str):
        """

        :param str playlist_id: the id of the playlist

        """

        if 'youtube.com' in playlist_id:
            self.id = re.findall(r'=(.*)',playlist_id)[0]
        else:
            self.id = playlist_id

    @property
    def info(self):
        """

        :return: a dict containing playlist info

        dict = {
                'name': name,
                'url': url,
                'video_count':video_count,
                'videos': videos,
                'thumbnail':thumb,
            }

        """

        try:
            url = f'https://www.youtube.com/playlist?list={self.id}'
            raw = urllib.request.urlopen(url).read().decode()

            name_data = re.findall(r"{\"title\":\"(.*?)\"",raw)
            name = name_data[0] if len(name_data) != 0 else None

            video_count_data = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"",raw)
            video_count = video_count_data[0] if len(video_count_data) != 0 else None

            thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)
            thumb = thumbnails[0] if len(thumbnails) != 0 else None

            videos = list(set(re.findall(r"videoId\":\"(.*?)\"", raw)))

            data_dict = {
                'name': name,
                'url': url,
                'video_count':video_count,
                'videos': videos,
                'thumbnail':thumb,
            }

            return data_dict

        except:
            return None


    @property
    def name(self):
        """

        :return: the name of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        name_data = re.findall(r"{\"title\":\"(.*?)\"", raw)
        return name_data[0] if len(name_data) != 0 else None


    @property
    def url(self):
        """

        :return: url of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        return url


    @property
    def video_count(self):
        """

        :return: total number of videos in that playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        video_count = re.findall(r"stats\":\[{\"runs\":\[{\"text\":\"(.*?)\"", raw)
        return video_count[0] if len(video_count) != 0 else None


    def videos(self, limit:int = None):
        """

        :param int limit: number of videos the user want from the playlist
        :return: list of < video objects > for each video in the playlist (consider limit)

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        videos = list(set(re.findall(r"videoId\":\"(.*?)\"", raw)))
        pure = Purify(limit=limit, iterable=videos)
        return [Video(item) for item in pure]

    def videos_as_url(self, limit:int = None):
        """

        :param int limit: number of video urls the user want from the playlist
        :return: list of urls for each video in the playlist (consider limit)

        """

        playList = Purify(limit=limit, iterable = self.videos())
        return [video.url for video in playList]


    @property
    def thumbnail(self):
        """

        :return: url of the thumbnail of the playlist

        """

        url = f'https://www.youtube.com/playlist?list={self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        thumbnails = re.findall(r"og:image\" content=\"(.*?)\?", raw)
        return thumbnails[0] if len(thumbnails) != 0 else None



class Video:

    def __init__(self, videoId:str):
        """

        :param videoId: video id or the url of the video

        """

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
        """

        :return: the title of the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"title\":\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None


    @property
    def views(self):
        """

        :return: total views the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"", raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def likes(self):
        """

        :return: total likes the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"\"label\":\"(.*?) likes\"", raw)
        return data[0] if len(data) != 0 else None


    @property
    def dislikes(self):
        """

        :return: total dislikes the video got so far

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def duration(self):
        """

        :return: total duration of  the video in milliseconds

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"approxDurationMs\":\"(.*?)\"",raw)
        return f'{data[0]}ms' if len(data) != 0 else None


    @property
    def upload_date(self):
        """

        :return: the date on which the video has been uploaded

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"uploadDate\":\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def channel_id(self):
        """

        :return: the id of the channel from which the video belongs

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"channelIds\":\[\"(.*?)\"",raw)
        return data[0] if len(data) != 0 else None


    @property
    def description(self):
        """

        :return: description provided with the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable",raw)
        return data[0] if len(data) != 0 else None


    @property
    def thumbnail(self):
        """

        :return: url of the thumbnail of the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            raw
        )
        return data[0] if len(data) != 0 else None


    @property
    def tags(self):
        """

        :return: list of tags used in video meta-data

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">",raw)
        return data[0].split(',') if len(data) != 0 else None


    @property
    def info(self):
        """

        :return: dict containing the the whole info of the video

        dict = {

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
        """

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
        """

        :param str keyword: the keyword to be searched

        """

        query = keyword.replace(" ", '+')
        self.parser = query


    @property
    def get_video(self):
        """

        :return: < video object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        video_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        return Video(video_ids[0]) if len(video_ids) != 0 else None


    @property
    def get_channel(self):
        """

        :return: < channel object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        channel_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        return Channel(channel_ids[0]) if len(channel_ids) != 0 else None


    def get_videos(self, limit: int = None):
        """

        :param int limit: total number of videos to be searched
        :return: list of < video object > of each video regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAQ%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"\"videoId\":\"(.*?)\"", raw)
        pureList = Purify(limit=limit, iterable=raw_ids)
        return [Video(item) for item in pureList] if len(pureList) != 0 else None


    def get_channels(self,limit:int = None):
        """

        :param int limit: total number of channels to be searched
        :return: list of < channel object > of each video regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAg%253D%253D'
        raw = urllib.request.urlopen(url).read().decode()
        raw_ids = re.findall(r"{\"channelId\":\"(.*?)\"", raw)
        pureList = Purify(limit=limit, iterable=raw_ids)
        return [Channel(item) for item in pureList] if len(pureList) != 0 else None


    @property
    def get_playlist(self):
        """

        :return: < playlist object > regarding the query

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAw%253D%253D'
        raw = urllib.request.urlopen(url=url).read().decode()
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        return Playlist(found[0]) if len(found) != 0 else None


    def get_playlists(self, limit:int = None):
        """

        :param int limit: total playlists be searched
        :return: list of < playlist object > of each playlist regarding the query (consider limit)

        """

        url = f'https://www.youtube.com/results?search_query={self.parser}&sp=EgIQAw%253D%253D'
        raw = urllib.request.urlopen(url=url).read().decode()
        found = re.findall(r"playlistId\":\"(.*?)\"", raw)
        pure = Purify(limit = limit, iterable = found)
        return [Playlist(item) for item in pure] if len(pure) != 0 else None



class Extras:

    def __init__(self):
        pass

    @property
    def Trending(self):
        """

        :return: < video object > of #1 on trending video

        """

        url = f'https://www.youtube.com/feed/trending'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return Video(data[0]) if len(data) != 0 else None


    @property
    def Music(self):
        """

        :return: list of < video object > of trending music videos

        """

        url = f'https://www.youtube.com/feed/music'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None


    @property
    def Gaming(self):
        """

        :return: list of < video object > of trending gaming videos

        """

        url = f'https://www.youtube.com/gaming'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def News(self):
        """

        :return: list of < video object > of trending news videos

        """

        url = f'https://www.youtube.com/news'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def Live(self):
        """

        :return: list of < video object > of trending livestreams

        """

        url = f'https://www.youtube.com/live'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None

    @property
    def Learning(self):
        """

        :return: list of < video object > of trending educational videos

        """

        url = f'https://www.youtube.com/learning'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None


    @property
    def Sports(self):
        """

        :return: list of < video object > of trending sports videos

        """
        url = f'https://www.youtube.com/sports'
        raw = urllib.request.urlopen(url).read().decode()
        data = re.findall(r"videoId\":\"(.*?)\"", raw)
        return [Video(item) for item in list(set(data))] if len(data) != 0 else None
