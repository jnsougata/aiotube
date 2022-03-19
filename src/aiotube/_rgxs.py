import re


class _ChannelPatterns:
    name = re.compile('channelMetadataRenderer\":{\"title\":\"(.*?)\"')
    id = re.compile('channelId\":\"(.*?)\"')
    verified = re.compile('"label":"Verified"')
    live = re.compile("thumbnailOverlays\":\[(.*?)]")
    video_id = re.compile('videoId\":\"(.*?)\"')
    uploads = re.compile("gridVideoRenderer\":{\"videoId\":\"(.*?)\"")
    subscribers = re.compile("}},\"simpleText\":\"(.*?) ")
    views = re.compile("viewCountText\":{\"simpleText\":\"(.*?)\"}")
    creation = re.compile("{\"text\":\"Joined \"},{\"text\":\"(.*?)\"}")
    country = re.compile("country\":{\"simpleText\":\"(.*?)\"}")
    custom_url = re.compile("canonicalChannelUrl\":\"(.*?)\"")
    description = re.compile("{\"description\":{\"simpleText\":\"(.*?)\"}")
    avatar = re.compile("height\":88},{\"url\":\"(.*?)\"")
    banner = re.compile("width\":1280,\"height\":351},{\"url\":\"(.*?)\"")
    playlists = re.compile("{\"url\":\"/playlist\?list=(.*?)\"")
    video_count = re.compile("videoCountText\":{\"runs\":\[{\"text\":(.*?)}")
    links = re.compile("q=https%3A%2F%2F(.*?)\"")
    upload_chunk = re.compile("gridVideoRenderer\":{(.*?)\"navigationEndpoint")
    upload_chunk_fl_1 = re.compile("simpleText\":\"Streamed")
    upload_chunk_fl_2 = re.compile("{\"text\":\" watching\"}]")
    upcoming_check = re.compile("\"title\":\"Upcoming live streams\"")
    upcoming = re.compile("gridVideoRenderer\":{\"videoId\":\"(.*?)\"")






