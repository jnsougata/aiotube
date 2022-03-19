from aiotube import Channel, Video, Playlist, Extras, Search

channels = Search.channels("spacex", limit=20).ids
print(channels)
