from aiotube import Channel, Video, Playlist, Extras, Search

channels = Search.playlists("spacex", limit=5).video_ids
print(channels)


# UC47rNmkDcNgbOcM-2BwzJTQ
#  {"runs":[{"text":"Scheduled for "}
#  gridVideoRenderer":{"videoId":"
#  "gridVideoRenderer\":{\"videoId\":\"(.*?)\""
