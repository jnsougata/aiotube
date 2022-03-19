from aiotube import Channel, Video, Playlist, Extras, Search

ch = Search.channels('AI')
print(ch.urls)
