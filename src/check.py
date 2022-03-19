from aiotube import Channel, Video, Playlist, Extras, Search

channels = Search.videos("spacex", limit=20).ids
print(channels)

