# aiotube

A library to access YouTube Public Data without YouTubeAPI

-   [Discord](https://discord.gg/Amx7z4EjuA)
-   [GitHub](https://github.com/jnsougata/aiotube)
# Table of Contents

-   [Installation](#installing)
-   [Building](#build-from-source)
-   [Quick Start](#quick-start)
-   [Usage](#usage)
-   [Channel](#channel)
-   [Video](#video)
-   [Playlist](#playlist)

## Installing

**Python 3.6 or higher is required**

``` sh
# Linux/macOS
python3 -m pip install -U aiotube
```

``` sh
# Windows
python -m pip install -U aiotube
```

## Build from source

``` sh
pip install git+https://github.com/jnsougata/aiotube
```

## Quick Start

``` py
import aiotube


channel = aiotube.Channel('@GYROOO')
print(channel.metadata)


video = aiotube.Video('WVDT4lSozHk')
print(video.metadata)


playlist = aiotube.Playlist('PL-xXQjd8X_Q-xXQjd8X_Q-xXQjd8X_Q-')
print(playlist.metadata)


search = aiotube.Search.video('YouTube Rewind 2018')
print(search.metadata)


search = aiotube.Search.channel('PewDiePie')
print(search.metadata)


search = aiotube.Search.playlist('Unlock Your Third Eye')
print(search.metadata)
```

## Usage

### Channel

| Property          | Return Type      | Description                                            |
|-------------------|------------------|--------------------------------------------------------|
| `live`            | `bool`           | Returns True if the channel is live                    |
| `streaming_now`   | `str`            | Returns the video id of the ongoing livestream         |
| `current_streams` | `List[str]`      | Returns a list of ids of ongoing livestreams           |
| `old_streams`     | `List[str]`      | Returns a list of ids of old livestreams               |
| `video_count`     | `int`            | Returns total number of videos uploaded by the channel |
| `upcoming`        | `Video`          | Returns a video object of the upcoming video           |
| `upcomings`       | `List[str]`      | Returns a list of ids of upcoming videos               |
| `playlists`       | `List[str]`      | Returns a list of playlist ids                         |
| `metadata`        | `Dict[str, Any]` | Returns the metadata of the channel in dict format     |
| `last_uploaded`   | `Video`          | Most recently uploaded video of the channel            |
| `last_streamed`   | `Video`          | Most recently completed livestream of the channel      |

| Method                        | Return Types | Description                                        |
|-------------------------------|--------------|----------------------------------------------------|
| `uploads(limit: int \| None)` | `List[str]`  | Returns a list of video ids of the uploaded videos |

### Video

| Properties | Return Types     | Description                                      |
|------------|------------------|--------------------------------------------------|
| `metadata` | `Dict[str, Any]` | Returns the metadata of the video in dict format |

### Playlist

| Properties | Return Types     | Description                                         |
|------------|------------------|-----------------------------------------------------|
| `metadata` | `Dict[str, Any]` | Returns the metadata of the playlist in dict format |

### Search

| Method                                     | Return Type | Description                                         |
|--------------------------------------------|-------------|-----------------------------------------------------|
| `channel(name: str)`                       | `Channel`   | Finds a channel with the given keywords             |
| `video(name: str)`                         | `Video`     | Finds a video with the given keywords               |
| `playlist(name: str)`                      | `Playlist`  | Finds a playlist with the given keywords            |
| `channels(name: str, limit: int \| None)`  | `List[str]` | Finds all channels that matches the given keywords  |
| `videos(name: str,  limit: int \| None)`   | `List[str]` | Finds all videos that matches the given keywords    |
| `playlists(name: str, limit: int \| None)` | `List[str]` | Finds all playlists that matches the given keywords |   

### Possible Exceptions 
| Class             | Description                                                     |
|-------------------|-----------------------------------------------------------------|
| `InvalidURL`      | Raised when then url is not a valid YouTube endpoint            |
| `TooManyRequests` | Raised when client IP receives soft ban from YouTube            |
| `RequestError`    | Raised for any type of request error not handled by the library |
