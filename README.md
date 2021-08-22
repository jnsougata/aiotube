# Ditch YouTube API

**DYA** (*Ditch YouTube API*) is a package created to get data of any YouTube Channel only by its Channel ID. ***No API Key is required.***

# How to use?

Currently is on development with limited usability! More methods will be added soon.

GitHub Repo **[LINK](https://github.com/jnsougata/Ditch-YouTube-API)**
 - **Installation:**
  `pip install dya`
  
 - **Importing DIA:**
 `from DIA import *`

 - **Creating an instance of the YouTube Channel:**
  `channel = DYA("YouTube_Channel_ID") `

 - **Attributes:**
 -  1. `is_live()` 
 
> Returns ***True*** if channel is Live at that moment, Otherwise
> returns ***False***

 -  2. `livestream_urls()`

> Returns ***List*** of Livestream Video URLs if channel is Live at that
> moment, Otherwise returns ***None***

 
 - 3. `latest_uploads(*limit)`
 
> Returns ***List*** of Latest Uploaded Video URLs if channel is not
> Live at that moment, Otherwise returns ***None***

 Examples:
 

        from DYA import * 

        channel = DYA('UCU9FEimjiOV3zN_5kujbCMQ')
        
        status = channel.is_live()
        livestreams = channel.livestream_urls()
        latestuploads = channel.latest_uploads(limit=5)
