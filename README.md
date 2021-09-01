# Ditch YouTube API (BETA)             
 **DYA** ( *Ditch YouTube API* ) is a package created to power the user with YouTube Data API functionality **without any API Key**  
  
 - **Got questions? Having issues? Join [Discord](https://discord.gg/YAFGAaMrTC)**  
 - # How to use?       
 - **Installation:**   
- `pip install dya`              
 - **Importing DYA:**   
- `from DYA import Search, Video, Channel`              
              
 - **Create an instance of target YouTube Channel:**   
- `channel = Channel("Channel ID/ Custom ID/ URL/ CustomURL") `         
 - **Attributes:**     
- `live`    
> Returns ***True*** if channel is Live at that moment, Otherwise returns ***False***              
 - `stream_link`     
> Returns ***URL*** of Livestream if channel is Live at that moment, otherwise returns ***None***              
 - `latest_uploads(*limit)`     
> Returns ***List*** of latest uploaded videos as **Video Object** if channel is not live at that moment, otherwise returns ***None***      
 - `info`  
 > Returns a **Dict** of the **About** of the YouTube Channel. Dict contains channel ***Name***, ***Subscribers***, ***Description***, ***Total Views***, ***Joining Date***, ***Country***, ***Custom URL***, ***Channel Avatar URL***,  ***Channel Banner URL***  
  - `playlists`     
> Returns a list of **Playlist Objects** of the channel's public playlists        
- Or, you can use **independent attributes** to get channel info:  
	 - `name` Returns **Name** of the channel or **None**  
	 - `id` Returns **ID** of the channel or **None**  
	 - `subs` Returns **Sub-count** of the channel or **None**      
	- `total_views` Returns total number of **Views** of the channel or **None**         
	- `joined_at` Returns channel **creation date** or **None**     
	- `country` Returns the generic country of the channel or **None**    
	- `custom_url` Returns the **Custom URL** of the channel or **None**     
	- `description` Returns the **Description** of the channel or **None**     
	- `avatar_url` Returns the **Avatar URL** of the channel or **None**     
	- `banner_url` Returns the **Banner URL** of the channel or **None**    
	
 - **Create an instance of YouTube Search:**        
- `Query = Search(*keywords: str)`  
   - ***Get Videos by YouTube Search:***     
		- `Result = Query.get_video`        
			> Returns a **Video Object** according to queries.    
		- `Results = Query.get_videos(*limit: int[optional])`        
			> Returns a list of **Video Objects** according to queries.  
			
	- ***Get Channels by YouTube Search:***        
		- `Result = Query.get_channel`        
			> Returns a **Channel Object** according to queries.    
		- `Results = Query.get_channels(*limit: int[optional])`        
			> Returns a list of **Channel Objects** according to queries.  
			
	- ***Get Playlists by YouTube Search:***   
		- `Result = Query.get_playlist`        
			> Returns a **Playlist Object** according to queries. 
			
 - **Create an instance of Video Data:**  
	 - `vid = Video("Video ID")`  
	 - **Attributes:**   
		- `info`   
			> Returns a **Dict** of video information [ **title**, **views**, **likes**, **dislikes**, **channel_id, duration**, **upload_date**, **thumbnail**, **tags** ]    
    
	- Or, you can use **independent attributes** to get each info individually:        
	   - `title` - Returns **title** of the video        
	   - `views` - Returns **view count** of the video        
	   - `likes` - Returns total **likes** on the video        
	   - `dislikes` -- Returns total **dislikes** on the video        
	   - `channel_id` - Returns **channel id** from which the video belong        
	   - `duration` -- Returns **duration** of the video        
	   - `upload_date` - Returns **date of upload** of the video        
	   - `description` - Returns whole **description** of the video        
	   - `tags` -- Returns **list of tags** of the video        
	   - `thumbnail` - Returns **HQ Thumbnail** of the video  
   
- **Create an instance of Playlist Data:**
	

    - `playlist = Playlist("playlist_id")`
    
    - **Attributes:**
	    - `info` 
		    > Returns a **dict** of info of the playlist containing playlist's ***name***, ***video count***, ***video ids***, ***thumbnail URL***, ***playlist URL***
		    
	- Or, you can use **independent attributes** to get each info individually:
		- `name` - Returns the **name** of the playlist or **None**
		- `url` - Returns the **URL** of the playlist or **None**
		- `video_count` - Returns the **video count** of the playlist or **None**
		- `videos` - Returns the list of **Video Objects** of the videos in playlist or **None**
		- `thumbnail` - Returns the **Thumbnail** of the playlist or **None**

  
 - **Create an instance of YouTube Extras:**  
	 - `extras = Extra()`  
	 
	  **Attributes:**  
	- `Trending` - Returns **#1 Trending** Video Object  
     - `Music` - Returns fresh trending list of ***Music*** Video Objects [ Video Object ]  
	 - `Gaming` - Returns fresh trending list of ***Gaming*** Video Objects [ Video Object ]  
	 - `News` - Returns fresh trending list of ***News*** Video Objects [ Video Object ]  
	 - `Live` - Returns fresh trending list of ***Live*** Video Objects [ Video Object ]  
	 - `Learning` - Returns fresh trending list of ***Educational*** Video Objects [ Video Object ]  
	 - `Sports` - Returns fresh trending list of ***Sports*** Video Objects [ Video Object ]
	 
