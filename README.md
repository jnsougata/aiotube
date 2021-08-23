 # Ditch YouTube API      
 **DYA** (*Ditch YouTube API*) is a package created to get data of any YouTube Channel only by its Channel ID. ***No API Key is required.***      
 # How to use?      
 Currently, it is on development with limited usability! More methods will be added soon.      
      
GitHub Repo **[LINK](https://github.com/jnsougata/Ditch-YouTube-API)**      
 - **Installation:** 
 - `pip install dya`      
 - **Importing DYA:** 
 - `from DYA import Channel, Search`      
      
 - **Creating an instance of target YouTube Channel:**
 - `channel = DYA("YouTube_Channel_ID") `   

  - **Methods:**      
- `is_live()` 
> Returns ***True*** if channel is Live at that moment, Otherwise > returns ***False***      
      
- `livesnow()`      
> Returns ***List*** of Livestream ***VideoIDs***  if channel is Live at that 
> moment, otherwise returns ***None***      
      
- `latest_uploads(*limit)` 
> Returns ***List*** of Latest Uploaded Video URLs if channel is not 
> Live at that moment, Otherwise returns ***None***      

- `about()` 
> Returns a **Dict** of the **About** of the YouTube Channel 
> Dict contains channel ***Name***, ***Subscribers***, ***Description***, ***TotalViews***, ***JoiningDate***, ***Country***, ***CustomURL***   
 - `playlists()`  
> Returns a List containing Ordered Pair **[ Name, ID ]** of public Playlists' ***List***

Or, you can use **independent methods** to get channel info:

 - `name()` Returns **Name** of the channel or **None** if not found.
 - `subs()` Returns **Sub-Count** of the channel or **None** if not found.
 - `total_views` Returns total number of **Views** of the channel or **None** if not found.
 - `joined_at()` Returns channel **creation date** or **None** if not found.
 - `country()` Returns the generic country of the channel or **None** if not found.
 - `custom_url()` Returns the **Custom URL** of the channel or **None** if not found.
 - `description()` Returns the **Description** of the channel or **None** if not found.
 - **Creating an instance of YouTube Search:**

	 - ***Getting videos by query:***
		 - `results = Search.get_videos(*keyword,*limit[optional])`
			 > Returns a list of **VideoIDs** according to queries.
	
	 - ***Getting channels by query:***
		 - `results = Search.get_channels(*keyword,*limit[optional])`
			 > Returns a list of **Channel IDs** according to queries.

