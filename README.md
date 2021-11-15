
# AioTube           
 **All in one Tube** is a package created to power the user with YouTube Data API functionality **without API Key**    
    
 - **[Discord](https://discord.gg/YAFGAaMrTC)** | **[GitHub](https://github.com/jnsougata/AioTube)**
# How to use?         
 - **Installation:**     
    - `pip install aiotube`  
    
 - **Importing AioTube:**     
    - `from aiotube import Search, Video, Channel, Playlist, Extras`   
   
 - **Create an instance of YouTube Channel:** 
   - 
     - `channel = Channel("channel Id / url / custom url") `    
            
     - **Method:**
        - `uploads(*limit:int [optional])`       
             > Returns ***bulk video Object*** of latest uploaded videos if channel is not live at that moment
     - **Attributes:** 
       - `id` Returns **id** of the channel or **None**
       - `info` Returns a **dict** of channel's information
       - `valid` Returns **True** if channel is valid else **False**
       - `name` Returns **name** of the channel or **None**
       - `live` Returns **True** if the channel is **Live**
       - `verified` Returns **True** if the channel is **Verified**
       - `livestream` Returns single **url** of newest occurring live stream or **None**
       - `livestreams` Returns list of **urls** of all occurring live streams or **None**
       - `oldstreams` Returns list of **urls** of old live streams or **None**
       - `latest` Returns **the latest Video (obj)** of the channel or **None**
       - `playlists` Returns **bulk playlist (obj)** of channel's public playlists
       - `subscribers` Returns **sub-count** of the channel or **None**        
       - `views` Returns total number of **views** of the channel or **None**           
       - `joined` Returns channel **creation date** or **None**       
       - `country` Returns the generic country of the channel or **None**      
       - `custom_url` Returns the **custom url** of the channel or **None**
       - `avatar` Returns the **avatar url** of the channel or **None**       
       - `banner` Returns the **banner url** of the channel or **None**  
       - `description` Returns channel's short **description** or **None**

 - **Get YouTube Search Results:**
   - 
     - **Get Videos by YouTube Search:**     
        - `Result = Search.video(*keywords: str)`   
		       
            > Returns a **Video Object** according to queries. 
			     
        - `Results = Search.videos(*keywords: str, *limit:int [optional])`   
		        
           > Returns a list of **Bulk Video Objects** according to queries.    
           
     - **Get Channels by YouTube Search:**    
       
        - `Result = Search.channel(*keywords: str)`          
             > Returns a **Channel Object** according to queries.     
		  
        - `Results = Search.channels(*keywords: str, *limit:int [optional])`          
	 
           > Returns a list of **Bulk Channel Objects** according to queries.    
           
     - **Get Playlists by YouTube Search:**    
        - `Result = Search.playlist(*keywords: str)`          
             > Returns a **Playlist Object** according to queries. 
		 
        - `Results = Search.playlists(*keywords: str, *limit:int [optional])`
            > Returns a list of **Bulk Playlist Objects** according to queries. 
		 
 - **Create an instance of Video Data:**
   - 
     - `vid = Video("video Id / video url")`
     - **Method:**
       - `download(format: str, filename: str[optional])`
         > use `mp3` or `mp4` as `format` [ downloads available best quality ]
       
     - **Attribute:**     
        - `info`     
         > Returns a **Dict** of video information **{ title, views, likes, dislikes, author, duration, upload_date, thumbnail, tags }** etc.      
      
     - **More Independent Attributes:**          
         - `title`  Returns **title** of the video          
         - `views`  Returns **view count** of the video          
         - `likes`  Returns total **likes** on the video          
         - `dislikes`  Returns total **dislikes** on the video          
         - `author`  Returns **channel id** from which the video belong          
         - `duration`  Returns **duration** of the video          
         - `uploaded`  Returns **date of upload** of the video                   
         - `url` Returns **url** of the video    
         - `thumbnail`  Returns **hq thumbnail** of the video  
         - `tags`  Returns **list of tags** of the video
         - `bytes` Returns the music file in **bytes** form     
 - **Create an instance of Playlist Data:** 
   - 
  
     - `playlist = Playlist("playlist id")`
  
     - **Attribute:**
   
        - `info`   
           > Returns a **dict** of info of the playlist containing playlist's ***name***, ***video count***, ***video ids***, ***thumbnail URL***, ***playlist URL***  
			
     - **More Independent Attributes:**
       - `name`  Returns the **name** of the playlist or **None**  
       - `url`  Returns the **url** of the playlist or **None**
       - `videos`  Returns the list of **video Objects** of the videos in playlist or **None**
       - `video_count`  Returns the **video count** of the playlist or **None**  
       - `thumbnail`  Returns the **thumbnail** of the playlist or **None**  
    
 - **Create an instance of YouTube Extras:**
   - 
      - `extras = Extras()`    
      
      - **Attributes:**    
         - `Trending`  Returns **#1 Trending** Video Object    
         - `Music`  Returns trending ***Music*** Video Objects **[bulk]**   
         - `Gaming`  Returns trending ***Gaming*** Video Objects **[bulk]**    
         - `News`  Returns trending ***News*** Video Objects **[bulk]**    
         - `Live`  Returns trending ***Live*** Video Objects **[bulk]**    
         - `Learning`  Returns trending ***Educational*** Video Objects **[bulk]**    
         - `Sports`  Returns trending ***Sports*** Video Objects **[bulk]**
