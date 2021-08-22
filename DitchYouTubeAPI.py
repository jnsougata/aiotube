import re
import urllib.request


class DYA:

    def __init__(self,CHANNELID):
        self.id = CHANNELID


    def get_data_for_live(self):
        url = f'https://www.youtube.com/channel/{self.id}'
        raw = urllib.request.urlopen(url).read().decode()
        return raw

    def get_data_for_latest_upload(self):
        url = f'https://www.youtube.com/channel/{self.id}'
        QUERY = f'{url}/videos'
        raw = urllib.request.urlopen(QUERY).read().decode()
        return raw


    def is_live(self):
        queryList = re.findall(r"\"text\":\" (\S{8})", self.get_data_for_live())
        if queryList[0] == 'watching':
            return True
        else:
            return False


    def livestream_urls(self):

        if self.is_live():
            VideoIDList = re.findall(r"watch\?v=(\S{11})", self.get_data_for_live())
            urls = [f'https://www.youtube.com/watch?v={ID}' for ID in VideoIDList]
            return urls
        else:
            return None


    def latest_uploads(self, limit:int = None):

        if self.is_live():
            return None
        else:
            VideoIDList = re.findall(r"watch\?v=(\S{11})", self.get_data_for_latest_upload())
            urls = [f'https://www.youtube.com/watch?v={ID}' for ID in VideoIDList]
            if limit is None:
                return urls
            else:
                num = int(len(urls) - limit)
                try:
                    return urls[:-num]
                except IndexError:
                    return urls


