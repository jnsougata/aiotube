
|Release|

.. |Release| image:: https://github.com/jnsougata/aiotube/actions/workflows/publish.yml/badge.svg
   :target: https://github.com/jnsougata/aiotube/actions/workflows/publish.yml

aiotube
==========

A library to access YouTube Public Data without YouTubeAPI

- `Discord <https://discord.gg/YAFGAaMrTC>`_
- `GitHub <https://github.com/jnsougata/AioTube>`_
- `REST API (BETA) <https://aiotube.deta.dev/>`_

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
    python -m pip install -U aiotube

Build from source
-----------------

.. code:: sh

    pip install git+https://github.com/jnsougata/aiotube

Quick Start
--------------

.. code:: py

    import aiotube


    channel = aiotube.Channel('UCU9FEimjiOV3zN_5kujbCMQ')
    print(channel.metadata)  # channel metadata in dict format


    video = aiotube.Video('WVDT4lSozHk')
    print(video.metadata)  # video metadata in dict format


    playlist = aiotube.Playlist('PL-xXQjd8X_Q-xXQjd8X_Q-xXQjd8X_Q-')
    print(playlist.metadata)  # playlist metadata in dict format


    search = aiotube.Search.video('YouTube Rewind 2018')
    print(search.metadata)  # searched video metadata in dict format


    search = aiotube.Search.channel('PewDiePie')
    print(search.metadata)  # searched channel metadata in dict format


    search = aiotube.Search.playlist('Unlock Your Third Eye')
    print(search.metadata)  # searched playlist metadata in dict format


Usage
------

Channel
~~~~~~~
.. csv-table::
   :header: "Method", "Return Type", "Description"
   :widths: 80, 80, 100


   "live()", "bool", "Returns True if the channel is live"
   "streaming_now()", "Video", "Returns the video the channel is streaming now"
   "current_streams()", "List[str]", "Returns a list of ids of currently streaming videos"
   "old_streams()", "List[str]", "Returns a list of ids of previously streaming videos"
   "video_count()", "int", "Returns the number of videos uploaded by the channel"
   "upcoming()", "Video", "Returns a video object of the upcoming video"
   "upcomings()", "List[str]", "Returns a list of ids of upcoming videos"
   "playlists()", "List[str]", "Returns a Playlist object"
   "uploads(limit: int)", "List[str]", "Returns a list of video ids of the uploaded videos"
   "last_uploaded()", "Video", "Video object of the most recently uploaded video"
   "last_streamed()", "Video", "Video object of the most recently streamed video"

.. csv-table::
   :header: "Properties", "Return Types", "Description"
   :widths: 80, 80, 100

   "metadata", "dict", "Returns the metadata of the channel in dict format"


Video
~~~~~
.. csv-table::
   :header: "Properties", "Return Types", "Description"
   :widths: 80, 80, 100

   "metadata", "Dict[str, Any]", "dictionary of video metadata"


Playlist
~~~~~~~~
.. csv-table::
   :header: "Property", "Return Type", "Description"
   :widths: 80, 80, 100

    "metadata", "Dict[str, Any]", "dictionary of playlist metadata"


Search
~~~~~~~~
.. csv-table::
   :header: "Methods", "Return Types", "Description"
   :widths: 80, 80, 100

   "channel(name: str)", "Channel", "Channel object of the channel with the given keywords"
   "video(name: str)", "Video", "Video object of the video with the given keywords"
   "playlist(name: str)", "Playlist", "Playlist object of the playlist with the given keywords"
   "channels(name: str, limit: int)", "List[str]", "list of channel ids of the channels found with the given keywords"
   "videos(name: str, limit: int)", "List[str]", "list of video ids of the videos found with the given keywords"
   "playlists(name: str, limit: int)", "List[str]", "list of playlist ids of the playlists found with the given keywords"
