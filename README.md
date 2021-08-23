
  
# Ditch YouTube API    
 **DYA** (*Ditch YouTube API*) is a package created to power the user with YouTube Data API functionality without any API Key.
 # How to use?    
 Currently, it is on development with limited usability! More methods will be added soon.    
    
 - **Installation:**    
- `pip install dya`    
 - **Importing DIA:**    
- `from DIA import *`    
    
 - **Creating an instance of target YouTube Channel:**    
- `channel = DYA("YouTube_Channel_ID") `    

    
 - **Attributes:**    
 - `is_live()`     
> Returns ***True*** if channel is Live at that moment, Otherwise   
> returns ***False***    
    
 - `livesnow()`    
 > Returns ***List*** of Livestream Video URLs if channel is Live at that > moment, Otherwise returns ***None***    
    
 - `latest_uploads(*limit)`    
> Returns ***List*** of Latest Uploaded Video URLs if channel is not > Live at that moment, Otherwise returns ***None***    
    
 - `about()`  
> Returns a **Dict** of the **About** of the YouTube Channel  
> Dict contains channel ***Name***, ***Subscribers***, ***Description***, ***TotalViews***, ***JoiningDate***, ***Country***, ***CustomURL***  

 - `playlists()`
> Returns a List containing the **URLs** of public playlist of the channel with **Playlist Names**

 
  **Examples:**    
   

    from DYA import * 
    channel = DYA('UCU9FEimjiOV3zN_5kujbCMQ') 
    status = channel.is_live() 
    livestreams = channel.livesnow() 
    latestuploads = channel.latest_uploads(limit=5) 
    about = channel.about()
    playlists = channel.playlists
