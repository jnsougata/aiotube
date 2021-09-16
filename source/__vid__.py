import re
import asyncio
import urllib.request
import concurrent.futures
from .__proc__ import _duration


class Video:

    def __init__(self, videoId: str):

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
        return data[0][:-6] if len(data) != 0 else None

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
        data = re.findall(r"approxDurationMs\":\"(.*?)\"", raw)

        return _duration(int(int(data[0]) / 1000)) if len(data) != 0 else None

    @property
    def upload_date(self):

        """

        :return: the date on which the video has been uploaded

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"uploadDate\":\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def parent(self):

        """

        :return: the id of the channel from which the video belongs

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"channelIds\":\[\"(.*?)\"", raw)
        return data[0] if len(data) != 0 else None

    @property
    def description(self):

        """

        :return: description provided with the video

        """

        raw = urllib.request.urlopen(self.url).read().decode()
        data = re.findall(r"shortDescription\":\"(.*)\",\"isCrawlable", raw)
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
        data = re.findall(r"<meta name=\"keywords\" content=\"(.*?)\">", raw)
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
            'duration':duration_data,
            'parent':id_data,
            'uploaded':date_data,
            'url':self.url,
            'thumbnail':thumb_data,
            'tags':tags,
        }

        """

        raw = urllib.request.urlopen(self.url).read().decode()

        async def _get_data(response, pattern):
            data = re.findall(pattern, response)
            return data[0] if len(data) > 0 else None

        patterns = [

            r"\"title\":\"(.*?)\"",
            r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\"",
            r"\"label\":\"(.*?) likes\"",
            r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\"",
            r"approxDurationMs\":\"(.*?)\"",
            r"channelIds\":\[\"(.*?)\"",
            r"uploadDate\":\"(.*?)\"",
            r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"",
            r"<meta name=\"keywords\" content=\"(.*?)\">"

        ]

        async def _main():
            tasks = []
            for pattern in patterns:
                task = asyncio.ensure_future(_get_data(raw, pattern))
                tasks.append(task)

            return await asyncio.gather(*tasks)

        ls = asyncio.run(_main())

        infoDict = {

            'title': ls[0],
            'id': self.id,
            'views': ls[1][:-6],
            'likes': ls[2],
            'dislikes': ls[3],
            'duration': _duration(int(int(ls[4]) / 1000)),
            'parent': ls[5],
            'uploaded': ls[6],
            'url': self.url,
            'thumbnail': ls[7],
            'tags': ls[8].split(','),

        }

        return infoDict

    @classmethod
    def bulk_title(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"\"title\":\"(.*?)\""
                    data.append(re.findall(pattern, response.read().decode())[0])
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_views(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"\"videoViewCountRenderer\":{\"viewCount\":{\"simpleText\":\"(.*?)\""
                    views = re.findall(pattern, response.read().decode())
                    data.append(views[0][:-6] if len(views) > 0 else None)
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_likes(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"label\":\"(.*?) likes\""
                    likes = re.findall(pattern, response.read().decode())
                    data.append(likes[0] if len(likes) > 0 else None)
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_dislikes(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"DISLIKE\"},\"defaultText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.*?) dislikes\""
                    dislikes = re.findall(pattern, response.read().decode())
                    data.append(dislikes[0] if len(dislikes) > 0 else None)
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_duration(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"approxDurationMs\":\"(.*?)\""
                    data.append(_duration(int(int(re.findall(pattern, response.read().decode())[0]) / 1000)))
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_upload_date(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"uploadDate\":\"(.*?)\""
                    data.append(re.findall(pattern, response.read().decode())[0])
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_parent(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"channelIds\":\[\"(.*?)\""
                    data.append(re.findall(pattern, response.read().decode())[0])
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_description(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"shortDescription\":\"(.*)\",\"isCrawlable"
                    desc = re.findall(pattern, response.read().decode())
                    data.append(desc[0] if len(desc) > 0 else None)
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_thumbnail(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"playerMicroformatRenderer\":{\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\""
                    data.append(re.findall(pattern, response.read().decode())[0])
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_tag(cls, ObjectList: list):

        async def _main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                ls = asyncio.get_event_loop()
                futures = [
                    ls.run_in_executor(
                        executor,
                        urllib.request.urlopen,
                        i.url
                    ) for i in ObjectList
                ]
                data = []
                for response in await asyncio.gather(*futures):
                    pattern = r"<meta name=\"keywords\" content=\"(.*?)\">"
                    tags = re.findall(pattern, response.read().decode())
                    data.append(tags[0].split(',') if len(tags) > 0 else None)
            return data

        return asyncio.run(_main())

    @classmethod
    def bulk_url(cls, ObjectList: list):
        return [i.url for i in ObjectList]

    @classmethod
    def bulk_id(cls, ObjectList: list):
        return [i.id for i in ObjectList]

