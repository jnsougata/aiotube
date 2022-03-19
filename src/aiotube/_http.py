from .auxiliary import _src, create_http_pool


def get_channel_about(head: str) -> str:
    url = head + '/about'
    return _src(url)


def get_channel_live_data(head: str) -> str:
    url = head + '/videos?view=2&live_view=501'
    return _src(url)


def get_old_streams(head: str) -> str:
    url = head + '/videos?view=2&live_view=503'
    return _src(url)


def get_uploads_data(head: str) -> str:
    url = head + '/videos?view=0&sort=dd&flow=grid'
    return _src(url)


def get_channel_playlists(head: str) -> str:
    url = head + '/playlists'
    return _src(url)


def get_upcoming_videos(head: str) -> str:
    url = head + '/videos?view=2&live_view=502'
    return _src(url)


def get_video_count(channel_id: str) -> str:
    url = f'https://www.youtube.com/results?search_query={channel_id}&sp=EgIQAg%253D%253D'
    return _src(url)

