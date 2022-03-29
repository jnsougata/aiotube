aiotube
==========

A library to access YouTube Public Data without YouTubeAPI

- `Discord <https://discord.gg/YAFGAaMrTC>`_
- `GitHub <https://github.com/jnsougata/AioTube>`_

Table of Contents
=================
- `Installation <#installing>`_
- `Building <#build-from-source>`_
- `Quick Start <#quick-start>`_
- `Usage <#usage>`_
- `Channel <#channel>`_
- `Video <#video>`_
- `Playlist <#playlist>`_


Installing
----------

**Python 3.6 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U aiotube

.. code:: sh

    # Windows
    py -3 -m pip install -U aiotube

Build from source
-----------------

.. code:: sh

    pip install git+https://github.com/jnsougata/aiotube

Quick Start
--------------

.. code:: py

    import aiotube


    channel = aiotube.Channel('UCU9FEimjiOV3zN_5kujbCMQ')

    print(channel.name)
    print(channel.description)
    print(channel.views)
    print(channel.subscribers)
    # and so on...
    # or
    print(channel.info) # dictionary of all basic info about the channel


    video = aiotube.Video('WVDT4lSozHk')

    print(video.title)
    print(video.description)
    print(video.views)
    print(video.likes)
    # and so on...
    # or
    print(video.info) # dictionary of all basic info about the video


    playlist = aiotube.Playlist('PL-xXQjd8X_Q-xXQjd8X_Q-xXQjd8X_Q-')

    print(playlist.name)
    print(playlist.url)
    print(playlist.video_count)
    # and so on...
    # or
    print(playlist.info) # dictionary of all basic info about the playlist


    search = aiotube.Search.video('YouTube Rewind 2018')

    print(search.title)
    print(search.description)
    print(search.views)
    print(search.likes)
    # and so on...
    # or
    print(search.info) # dictionary of all basic info about the video


    search = aiotube.Search.channel('PewDiePie')

    print(search.name)
    print(search.description)
    print(search.views)
    print(search.subscribers)
    # and so on...
    # or
    print(search.info) # dictionary of all basic info about the channel


    search = aiotube.Search.playlist('Unlock Your Third Eye')

    print(search.name)
    print(search.url)
    print(search.video_count)
    # and so on...
    # or
    print(search.info) # dictionary of all basic info about the playlist


Usage
------

Channel
~~~~~~~
.. csv-table::
   :header: "Method", "Return Type", "Description"
   :widths: 80, 80, 100

   "uploads(limit: int)", "Dict", "info dict of videos uploaded by the channel"

.. csv-table::
   :header: "Attribute", "Return Type", "Description"
   :widths: 80, 80, 100

   "id", "str", "unique id of the channel"
   "name", "str", "name of the channel"
   "verified", "bool", "whether the channel is verified"
   "description", "str", "description of the channel"
   "views", "str", "total number of views of the channel"
   "video_count", "str", "number of videos in the channel"
   "country", "str", "country of the channel"
   "custom_url", "str", "custom url of the channel"
   "created_at", "str", "date of the channel creation"
   "subscribers", "str", "number of subscribers of the channel"
   "avatar", "str", "url of the avatar of the channel"
   "banner", "str", "url of the banner of the channel"
   "valid", "bool", "whether the channel is valid or not"
   "info", "Dict[str, Any]", "dictionary of all basic info about the channel"
   "links", "list", "list of all links added to the channel"
   "live", "bool", "whether the channel is live or not"
   "latest", "Video", "most latest video of the channel"
   "livestream", "Live", "Live object of the newest livestream"
   "livestreams", "List", "list of occurring livestream ids of the channel"
   "old_streams", "Dict[str, Dict[str, Any]]", "info dict of the old streams"
   "recent_uploaded", "Video", "Video object of the most recently uploaded video"
   "recent_streamed", "Video", "Video object of the most recently streamed video"
   "upcoming", "Upcoming", "Upcoming object of the upcoming video of the channel"
   "all_upcoming", "List", "list of upcoming video ids of the channel"
   "playlists", "Dict[str, Dict[str, Any]]", "info dict of the playlists of the channel"


Video
~~~~~
.. csv-table::
   :header: "Attribute", "Return Type", "Description"
   :widths: 80, 80, 100

   "id", "str", "unique id of the video"
   "title", "str", "title of the video"
   "url", "str", "url of the video"
   "description", "str", "description of the video"
   "views", "str", "total number of views of the video"
   "likes", "str", "number of likes of the video"
   "duration", "float", "duration of the video in seconds"
   "thumbnail", "str", "url of the thumbnail of the video"
   "upload_date", "str", "date of the video upload"
   "author", "str", "id of the channel where the video was uploaded"
   "tags", "List[str]", "list of tags of the video"
   "info", "Dict[str, Any]", "dictionary of all basic info about the video"
   "premiered", "bool", "whether the video was premiere or not"
   "streamed", "bool", "whether the video was streamed or not"


Playlist
~~~~~~~~
.. csv-table::
   :header: "Attribute", "Return Type", "Description"
   :widths: 80, 80, 100

   "id", "str", "unique id of the playlist"
   "name", "str", "name of the playlist"
   "url", "str", "url of the playlist"
   "video_count", "str", "number of videos in the playlist"
   "videos", "Dict[str, Dict[str, Any]]", "info dict of the videos in the playlist"
   "thumbnail", "str", "url of the thumbnail of the playlist"
   "info", "Dict[str, Any]", "dictionary of all basic info about the playlist"


Search
~~~~~~~~
.. csv-table::
   :header: "Method", "Return Type", "Description"
   :widths: 80, 80, 100

   "channel(name: str)", "Channel", "Channel object of the channel with the given keywords"
   "video(name: str)", "Video", "Video object of the video with the given keywords"
   "playlist(name: str)", "Playlist", "Playlist object of the playlist with the given keywords"
   "channels(name: str, limit: int)", "Dict[str, Dict[str, Any]]", "info dict of the channels with the given keywords"
   "videos(name: str, limit: int)", "Dict[str, Dict[str, Any]]", "info dict of the videos with the given keywords"
   "playlists(name: str, limit: int)", "Dict[str, Dict[str, Any]]", "info dict object of the playlists with the given keywords"
