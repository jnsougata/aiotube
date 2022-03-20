from .utils import _fetch_webpage, parser


def _get_channel_about(head: str) -> str:
    url = head + '/about'
    return _fetch_webpage(url)


def _get_channel_live_data(head: str) -> str:
    url = head + '/videos?view=2&live_view=501'
    return _fetch_webpage(url)


def _get_old_streams(head: str) -> str:
    url = head + '/videos?view=2&live_view=503'
    return _fetch_webpage(url)


def _get_uploads_data(head: str) -> str:
    url = head + '/videos?view=0&sort=dd&flow=grid'
    return _fetch_webpage(url)


def _get_channel_playlists(head: str) -> str:
    url = head + '/playlists'
    return _fetch_webpage(url)


def _get_upcoming_videos(head: str) -> str:
    url = head + '/videos?view=2&live_view=502'
    return _fetch_webpage(url)


def _get_video_count(channel_id: str) -> str:
    head = 'https://www.youtube.com/results?search_query='
    tail = '&sp=EgIQAg%253D%253D'
    url = head + channel_id + tail
    return _fetch_webpage(url)


def _get_video_data(video_id: str) -> str:
    url = f'https://www.youtube.com/watch?v={video_id}'
    return _fetch_webpage(url)


def _get_playlist_data(playlist_id: str) -> str:
    url = 'https://www.youtube.com/playlist?list=' + playlist_id
    return _fetch_webpage(url)


def _get_trending_video() -> str:
    return _fetch_webpage('https://www.youtube.com/feed/trending')


def _get_trending_songs() -> str:
    return _fetch_webpage('https://www.youtube.com/feed/music')


def _get_trending_gaming_videos() -> str:
    return _fetch_webpage('https://www.youtube.com/gaming')


def _get_trending_news_feeds() -> str:
    return _fetch_webpage('https://www.youtube.com/news')


def _get_trending_streams() -> str:
    return _fetch_webpage('https://www.youtube.com/live')


def _get_trending_learning_videos() -> str:
    return _fetch_webpage('https://www.youtube.com/learning')


def _get_trending_sports_videos() -> str:
    return _fetch_webpage('https://www.youtube.com/sports')


def _find_videos(query: str) -> str:
    head = 'https://www.youtube.com/results?search_query='
    tail = '&sp=EgIQAQ%253D%253D'
    parsed_query = parser(query)
    return _fetch_webpage(head + parsed_query + tail)


def _find_channels(query: str) -> str:
    head = 'https://www.youtube.com/results?search_query='
    tail = '&sp=EgIQAg%253D%253D'
    parsed_query = parser(query)
    return _fetch_webpage(head + parsed_query + tail)


def _find_playlists(query: str) -> str:
    head = 'https://www.youtube.com/results?search_query='
    tail = '&sp=EgIQAw%253D%253D'
    parsed_query = parser(query)
    return _fetch_webpage(head + parsed_query + tail)
