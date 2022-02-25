import re


class Streams:
    def __init__(self, urls: list[str]):
        self.__urls = urls

    @property
    def audio_streams(self) -> list[str]:
        return [url for url in self.__urls if 'mime=audio' in url]

    @property
    def best_audio(self) -> str:
        for url in self.audio_streams:
            if 'mime=audio/mp4' in url:
                return url

    @property
    def video_streams(self) -> list[str]:
        return [url for url in self.__urls if 'itags' in url]
