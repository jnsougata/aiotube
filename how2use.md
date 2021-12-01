# **__Welcome to the `official aiotube guide`__**
This guide will walkthrough the different ways to use aiotube

## Table of Content
- [Aiotube](#aiotube)
  - [Installation](#installation)
  - [Getting started](#getting_started)
  - [Search](#search)
    - [Video](#search_video)
      - [Basics](#search_video_basics)
      - [Attributes](#search_video_attributes)
      - [Bulk](#search_video_bulk)
    - [Channel](#search_channel)
      - [Attributes](#search_channel_attributes)
      - [Uploads](#search_channel_uploads)
      - [Bulk](#search_channel_bulk)
    - [Playlist](#search_playlist)
      - [Attributes](#search_playlist_attributes)
      - [Bulk](#search_playlist_bulk)
   - [Video](#video) 
     - [Basics](#video_basics)
     - [Attributes](#video_attributes)
     - [Dict](#video_dict)
   - [Channel](#channel) 
     - [Attributes](#channel_attributes)
   - [Playlist](#playlist) 
     - [Attributes](#playlist_attributes)
   - [Extras](#extras) 
     - [Attributes](#extras_attributes)
- [The end](#end)

## <a name="aiotube"></a> Aiotube

All in One Tube is a package created to power the user with YouTube Data API v3 
functionality without API Key. Only valid for public information.

**Related Links:**
> [`PyPi`](https://pypi.org/project/aiotube/)
> 
> [`Code(Github)`](https://github.com/jnsougata/AioTube)
> 
> [`Support Server(Discord)`](https://discord.gg/YAFGAaMrTC)
> 
> [`Gist Creator`](https://slumberdemon.carrd.co)

## <a name="installation"></a> Installation

````
pip install aiotube
````

## <a name="getting_started"></a> Getting Started

```py
# Imports everything (Search, Vide, Channel, Playlist, Extras)
# This guide will use *

from aiotube import *

# Imports individual options

from aiotube import Search, Video, Channel, Playlist, Extras
```


## <a name="search"></a> YouTube Search

#### <a name="search_video"></a> Get Videos by YouTube Search

###### <a name="search_video_basics"></a> Basics

This will get the first video from youtube search results

```py
from aiotube import *

Video = Search.video(keywords='youtube rewind')
```

Now if we `print(Video)` we will get something like this:
```
<aiotube._video.Video object at 0x7fed958807c0>

```

This is not exactly what we want though so to get the video url we have to use the `url` attribute

```py
from aiotube import *

Video = Search.video(keywords='youtube rewind')

print(Video.url)
```
This will output the following:
```
https://www.youtube.com/watch?v=YbJOTdZBX1g
```

###### <a name="search_video_attributes"></a> Attributes

To get more information on the video we can use the following attributes: `title`, `views`, `likes`, `dislikes`(This property is deprecated as YouTube is slowly removing public dislike counts), `author`, `duration`, `url`, `thumbnail`, `tags`

```py
from aiotube import *

Video = Search.video('youtube rewind')

print(Video.title)
print(Video.views)
print(Video.likes)
print(Video.author)
print(Video.duration)
print(Video.url)
print(Video.thumbnail)
print(Video.tags)
```

This will output:

```
YouTube Rewind 2018: Everyone Controls Rewind | #YouTubeRewind 
221,872,774 
3,064,001
UCBR8-60-B28hp2BmDPdntcQ
0h 8m 13s
https://www.youtube.com/watch?v=YbJOTdZBX1g
https://i.ytimg.com/vi/YbJOTdZBX1g/maxresdefault.jpg
['Rewind', ' Rewind 2018', ' youtube rewind 2018', ' #YouTubeRewind', ' Rewind 2017', ' Lilly Singh', ' Markiplier', ' Swoozie', ' Liza Koshy', ' Dolan Twins', ' Lele Pons', ' Rudy Mancuso', ' Casey Neistat', ' LaurDIY', ' Merrell Twins', ' Collins Key', ' Safiya Nygaard', ' Luisito Comunica', ' BB Ki Vines', ' Bie The Ska', ' Authentic Games', ' Manual do Mundo', ' Fortnite', ' Kiki Challenge', ' Mukbang', ' Ninja', ' BTS', ' Idol', ' Marshmello', ' Cardi B', ' Year in Review', ' In my feelings challenge']
```

###### <a name="search_video_bulk"></a> Bulk

You can also get videos in bulk. Even though their is no limit to the search aiotube wont return the exact amount, as it has to load the full page. Bulk video search also has some attributes: `ids`, `urls`, `views`, `likes`, `dislikes`(This property is deprecated as YouTube is slowly removing public dislike counts), `durations`, `dates`, `parents`, `descriptions`, `thumbnails`, `tags`

```py
from aiotube import *

Videos = Search.videos('youtube rewind', limit=100)

print(Videos.ids)
print(Videos.urls)
print(Videos.views)
print(Videos.likes)
print(Videos.durations)
print(Videos.dates)
print(Videos.parents)
print(Videos.descriptions)
```

Output:

```
['YbJOTdZBX1g', 'PKtnafFtfEo', '2lAe1cqCOXo', 'FlsCjmMhFmw', 'FKmgrY1zfuw', 'KK9bwTlAvgo', '_GuOjXYl5ew', 'H7jtC8vjXw8', 'zKx2B8WCQuw', 'By_Cn5ixYLg', 'iCkYw3cRwLo', 'P5dxd-ocaE8', 'SmnkYyHQqNs', '3AL2UkOn-Ow', 'Ek92ri3lJz4', 'TgEI_XobnhE', 'UFnXm6cjGwU', 'I2Qs-inYgp8', 'Z-JkdGYAHl4', 'BXc0W_fibYc']
['https://www.youtube.com/watch?v=YbJOTdZBX1g', 'https://www.youtube.com/watch?v=PKtnafFtfEo', 'https://www.youtube.com/watch?v=2lAe1cqCOXo', 'https://www.youtube.com/watch?v=FlsCjmMhFmw', 'https://www.youtube.com/watch?v=FKmgrY1zfuw', 'https://www.youtube.com/watch?v=KK9bwTlAvgo', 'https://www.youtube.com/watch?v=_GuOjXYl5ew', 'https://www.youtube.com/watch?v=H7jtC8vjXw8', 'https://www.youtube.com/watch?v=zKx2B8WCQuw', 'https://www.youtube.com/watch?v=By_Cn5ixYLg', 'https://www.youtube.com/watch?v=iCkYw3cRwLo', 'https://www.youtube.com/watch?v=P5dxd-ocaE8', 'https://www.youtube.com/watch?v=SmnkYyHQqNs', 'https://www.youtube.com/watch?v=3AL2UkOn-Ow', 'https://www.youtube.com/watch?v=Ek92ri3lJz4', 'https://www.youtube.com/watch?v=TgEI_XobnhE', 'https://www.youtube.com/watch?v=UFnXm6cjGwU', 'https://www.youtube.com/watch?v=I2Qs-inYgp8', 'https://www.youtube.com/watch?v=Z-JkdGYAHl4', 'https://www.youtube.com/watch?v=BXc0W_fibYc']
['221,879,265', '55,820,138', '117,730,214', '239,126,586', '2,642,678', '155,027,456', '241,802,596', '136,768,103', '135,296,656', '83,916,587', '194,627,855', '7,699,323', '12,767,064', '3,595,641', '1,747,783', '1,153,977', '6,924,847', '6,330,116', '4,609,727', '209,790']
['3,064,047', '4,658,525', '3,490,724', '4,672,800', '36,187', '3,007,845', '4,066,519', '1,676,413', '1,709,527', '9,545,442', '1,540,349', '373,396', '137,506', '150,554', '28,408', '60,017', '112,829', '144,113', '490,227', '11,987']
['0h 8m 13s', '0h 6m 30s', '0h 5m 36s', '0h 7m 14s', '1h 16m 9s', '0h 6m 39s', '0h 6m 52s', '0h 5m 46s', '0h 6m 35s', '0h 5m 34s', '0h 4m 14s', '0h 11m 10s', '0h 2m 19s', '0h 9m 6s', '0h 36m 49s', '0h 10m 24s', '0h 1m 25s', '0h 19m 19s', '0h 9m 18s', '0h 5m 17s']
['2018-12-06', '2021-01-01', '2019-12-05', '2017-12-06', '2021-01-12', '2015-12-09', '2016-12-07', '2013-12-11', '2014-12-09', '2018-12-27', '2012-12-17', '2018-12-12', '2011-12-20', '2017-12-25', '2018-12-06', '2019-12-06', '2010-12-13', '2019-01-24', '2021-11-11', '2021-11-23']
['UCBR8-60-B28hp2BmDPdntcQ', 'UCX6OQ3DkcsbYNE6H8uQQuVA', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCBR8-60-B28hp2BmDPdntcQ', 'UC0NaWwWghJD37rMK2AYDidg', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCBR8-60-B28hp2BmDPdntcQ', 'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCBJycsmduvYEL83R_U4JriQ', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCzUYuC_9XdUUdrnyLii8WYg', 'UCpOTGDMVBdzfPsrSYRXn-jQ', 'UCaWd5_7JhbQBe4dknZhsHJg', 'UCBR8-60-B28hp2BmDPdntcQ', 'UCKqH_9mk1waLgBiL2vT5b9g', 'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'UCnyR4T5qpgOrWGcQU6Jinkw']
["YouTube Rewind 2018. Celebrating the videos, people, music and moments that defined 2018. #YouTubeRewind  It wouldn’t be Rewind without the creators: https://rewind.youtube/creators Explore the videos, music and trends that defined YouTube in 2018: https://rewind.youtube  Watch the Behind the Scenes video: https://youtu.be/8qTQbk2A02M   See all the Easter Eggs: https://goo.gl/xr3uUn    Music by The Hood Internet YouTube Rewind 2018 produced by Portal A   Starring:  10Ocupados Adam Rippon Afros e Afins por Nátaly Neri Alisha Marie Ami Rodriguez  Anwar Jibawi AsapSCIENCE AuthenticGames BB Ki Vines Bearhug Bie The Ska Bilingirl Chika Bokyem TV CajuTV Casey Neistat Caspar Cherrygumms Collins Key Dagi Bee Desimpedidos Diva Depressão Dolan Twins Domics Dotty TV Elle Mills emma chamberlain Enes Batur EnjoyPhoenix EroldStory FAP TV FavijTV Fischer's Furious Jumper Gabbie Hanna GamingWithKev GEN HALILINTAR Gongdaesang gymvirtual Hannah Stocking HikakinTV How Ridiculous illymation ItsFunneh JaidenAnimations  James Charles John Oliver Jordindian  Jubilee Media JukiLop julioprofe Katya Zamolodchikova Kaykai Salaider  Kelly MissesVlog Krystal Yam \\u0026 family LA LATA Lachlan LaurDIY Lele Pons Life Noggin Lilly Singh Liza Koshy LosPolinesios Lucas the Spider Luisito Comunica (Rey Palomo) Luzu Lyna Manual do Mundo Markiplier  Marques Brownlee Marshmello Mason Ramsey Me Poupe! Merrell Twins Michael Dapaah  MissRemiAshten mmoshaya Molly Burke Ms Yeah Muro Pequeno Nick Eh 30 NikkieTutorials  Ninja Noor Stars  Pautips Pinkfong Baby Shark Pozzi Primitive Technology RobleisIUTU Rosanna Pansino Rudy Mancuso Safiya Nygaard Sam Tsui SamHarveyUK SHALOM BLAC Simone Giertz skinnyindonesian24 Sofia Castro  @StrayRogue and @DitzyFlama (Bongo Cat) sWooZie Tabbes Technical Guruji  The Try Guys TheKateClapp TheOdd1sOut Tiền Zombie v4  Trevor Noah Trixie Mattel Wengie WhinderssonNunes Will Smith Yammy  Yes Theory  All comments featured in Rewind inspired by real comments from the YouTube community.", 'This is what Youtube Rewind would look like if it was made by creators lol SUBSCRIBE TO THESE SMALL CHANNELS NOW PLEASE!!! NalterDeeds: https://www.youtube.com/user/nalterdeeds Amelia and Bridie: https://www.youtube.com/channel/UCrSTjIIkIBHL7VDx7utP56w Soyan Osman: https://www.youtube.com/channel/UCuPGqvywieBAqvbkMSF4CNQ  Thank you to these 3 boys for editing this video! I LOVE YOU GUYS AND AM FOREVER GRATEFUL! FlyingKitty: https://www.youtube.com/channel/UCYQT13AtrJC0gsM1far_zJg Dolan Dark: https://www.youtube.com/channel/UCI5qWAMf5PHLNcM13R8pfiQ Grandayy: https://www.youtube.com/channel/UCa6TeYZ2DlueFRne5DyAnyg    All creator sub data from SocialBlade https://socialblade.com/  ╔═╦╗╔╦╗╔═╦═╦╦╦╦╗╔═╗ ║╚╣║║║╚╣╚╣╔╣╔╣║╚╣═╣  ╠╗║╚╝║║╠╗║╚╣║║║║║═╣ ╚═╩══╩═╩═╩═╩╝╚╩═╩═╝ ---------------------------------------------------------------- follow all of these or i will kick you • Facebook - https://www.facebook.com/MrBeast6000/ • Twitter - https://twitter.com/MrBeast •  Instagram - https://www.instagram.com/mrbeast --------------------------------------------------------------------', "In 2018, we made something you didn’t like. For Rewind 2019, let’s see what you DID like.  Celebrating the creators, music and moments that mattered most to you in 2019.   To learn how the top lists in Rewind were generated: https://rewind.youtube/about  Top lists featured the following channels:  @1MILLION Dance Studio  @A4  @Anaysa  @Andymation  @Ariana Grande  @Awez Darbar  @AzzyLand  @Billie Eilish  @Black Gryph0n  @BLACKPINK  @ChapkisDanceUSA  @Daddy Yankee  @David Dobrik  @Dude Perfect  @Felipe Neto  @Fischer's-フィッシャーズ-  @Galen Hooks  @ibighit  @James Charles  @jeffreestar  @Jelly  @Kylie Jenner  @LazarBeam  @Lil Dicky  @Lil Nas X  @LOUD  @LOUD Babi  @LOUD Coringa  @Magnet World  @MrBeast  @Nilson Izaias Papinho Oficial  @Noah Schnapp @백종원의 요리비책 Paik's Cuisine  @Pencilmation  @PewDiePie  @SethEverman  @shane  @Shawn Mendes  @Team Naach  @whinderssonnunes  @워크맨-Workman  @하루한끼 one meal a day   To see the full list of featured channels in Rewind 2019, visit: https://rewind.youtube/about", 'YouTube Rewind 2017. Celebrating the videos, people, music and memes that made 2017. #YouTubeRewind  Meet the featured Creators in Rewind: https://rewind2017.withyoutube.com/creators Spend more time with your favorite Creators, videos and trends from 2017: https://yt.be/rewind2017 Test your Rewind knowledge with our trivia game: http://yt.be/dejaview  Watch trending videos from 2017: http://youtube.com/rewind See the trends as they happen: http://youtube.com/trending  Watch the Behind the Scenes video: https://youtu.be/OIQQ8jmsbMM   See all the Easter Eggs: https://goo.gl/3U9otg  Music by The Hood Internet: https://www.youtube.com/thehoodinternet  YouTube Rewind 2017 produced by Portal A', 'Click here to watch: \\"Thanksgiving 2021 - What Are They Thankful For? | JEFF DUNHAM\\"  https://www.youtube.com/watch?v=xPecKEBma9U --~-- The mostly garbage year of 2020 is now in the dumpster, and Walter, Peanut, Bubba J, Achmed, and I are certainly ready to move on!... (even though ‘21 is already looking like it’s going to be a doozy...☹️) Before we do, however, we thought it might be fun to take a look back at some of our top 2020 videos. Let’s rewind to some of our favorite uploads which hopefully helped get us through it all. 👍 Which one do you like the most!?  Stream my last comedy special, Jeff Dunham: Beside Himself on Netflix NOW! Woo hoo! http://smarturl.it/BesideHimself  Stream my comedy special, Jeff Dunham: Relative Disaster on Netflix! http://bit.ly/JeffDunham_RD  Like me on Facebook: http://www.facebook.com/JeffDunham Subscribe to my YouTube: http://bit.ly/SubscribeDunham Follow me on Twitter: http://www.twitter.com/JeffDunham \\u0026 Follow me on Instagram: http://www.instagram.com/JeffDunham  #JeffDunham #YouTubeRewind #2020  #ComedyCentral', "YouTube Rewind 2015. Celebrating the videos, people, music and moves that made 2015. #YouTubeRewind  Watch the year's trending videos: http://youtube.com/rewind See the trends as they happen on the new trending tab: http://youtube.com/trending Watch the BTS video: https://youtu.be/vY-c7efXiuM  Music by The Hood Internet https://www.youtube.com/thehoodinternet Featuring an original remix by Avicii https://www.youtube.com/AviciiOfficialVEVO  Alfie https://www.youtube.com/PointlessBlog Amanda Steele https://www.youtube.com/MakeupbyMandy24 amazingphil https://www.youtube.com/AmazingPhil Andy Raconte https://www.youtube.com/AndyRaconte Anna Akana https://www.youtube.com/AnnaAkana Barely Productions https://www.youtube.com/barelypolitical Bart Baker https://www.youtube.com/BartBaKer Bethany Mota https://www.youtube.com/Macbarbie07 BibisBeautyPalace https://www.youtube.com/BibisBeautyPalace The Try Guys https://www.youtube.com/BuzzFeedVideo Caeli https://www.youtube.com/CaELiKe Cameron Dallas https://www.youtube.com/TheeCameronDallas CaptainSparklez https://www.youtube.com/CaptainSparklez Casey Neistat https://www.youtube.com/caseyneistat Connor Franta https://www.youtube.com/ConnorFranta Cyprien https://www.youtube.com/MonsieurDream danisnotonfire https://www.youtube.com/danisnotonfire Dner https://www.youtube.com/DnerMC EeOneGuy https://www.youtube.com/EeOneGuy elrubiusOMG https://www.youtube.com/elrubiusOMG enchufeTV https://www.youtube.com/enchufetv The Fine Brothers https://www.youtube.com/TheFineBros Flula https://www.youtube.com/djflula FouseyTUBE https://www.youtube.com/fouseyTUBE Game Grumps https://www.youtube.com/GameGrumps The Game Theorists https://www.youtube.com/MatthewPatrick13 Gigi Gorgeous https://www.youtube.com/GregoryGORGEOUS GloZell Green https://www.youtube.com/glozell1 Grace Helbig https://www.youtube.com/graciehinabox The Gregory Brothers https://www.youtube.com/thegregorybrothers Hajime https://www.youtube.com/0214mex Hannah Hart https://www.youtube.com/MyHarto Heaven King https://www.youtube.com/beautee132 HolaSoyGerman https://www.youtube.com/HolaSoyGerman iHasCupquake https://www.youtube.com/iHasCupquake iJustine https://www.youtube.com/ijustine Ingrid Nilsen https://www.youtube.com/missglamorazzi James Corden https://www.youtube.com/TheLateLateShow Jenna Marbles https://www.youtube.com/JennaMarbles Jennxpenn https://www.youtube.com/jennxpenn Joey Graceffa https://www.youtube.com/JoeyGraceffa John Oliver https://www.youtube.com/LastWeekTonight Julienco https://www.youtube.com/juliencotv Karlie Kloss https://www.youtube.com/karliekloss Kingsley https://www.youtube.com/ItsKingsleyBitch Kurt Hugo Schneider https://www.youtube.com/KurtHugoSchneider LaurDIY https://www.youtube.com/LaurDIY LeFloid https://www.youtube.com/LeFloid Lohanthony https://www.youtube.com/lohanthony Malena https://www.youtube.com/malena010102 Mamrie Hart https://www.youtube.com/YouDeserveADrink Markiplier https://www.youtube.com/markiplierGAME Matthew Santoro https://www.youtube.com/MatthewSantoro Miranda Sings https://www.youtube.com/mirandasings08 Marques Brownlee https://www.youtube.com/marquesbrownlee MyLifeAsEva https://www.youtube.com/mylifeaseva Norman Thavaud https://www.youtube.com/NormanFaitDesVideos OMGitsFirefoxx https://www.youtube.com/OMGitsfirefox OMI https://www.youtube.com/omishangrecords PewDiePie https://www.youtube.com/PewDiePie Los Polinesios https://www.youtube.com/LosPolinesios Porta dos Fundos https://www.youtube.com/portadosfundos PrankvsPrank https://www.youtube.com/PrankvsPrank Rclbeauty https://www.youtube.com/Rclbeauty101 Ray William Johnson https://www.youtube.com/RayWilliamJohnson Rebecca Black https://www.youtube.com/rebecca Rhett \\u0026 Link https://www.youtube.com/RhettandLink Rhodes Bros https://www.youtube.com/TheRhodesBros Ricky Dillon https://www.youtube.com/PICKLEandBANANA Ro Pansino https://www.youtube.com/RosannaPansino Rob Dyke https://www.youtube.com/TheRobDyke Slow Mo Guys https://www.youtube.com/theslowmoguys Smosh https://www.youtube.com/smosh Smosh Games https://www.youtube.com/SmoshGames Sophia Grace https://www.youtube.com/SophiaGraceBrownlee Squeezie https://www.youtube.com/aMOODIEsqueezie ||Superwoman|| https://www.youtube.com/IISuperwomanII Swoozie https://www.youtube.com/swoozie06 T-Pain https://www.youtube.com/TPainVEVO TheViralFever https://www.youtube.com/TheViralFeverVideos The Young Turks https://www.youtube.com/TheYoungTurks Timothy DeLaGhetto https://www.youtube.com/TimothyDeLaGhetto2 Todrick Hall https://www.youtube.com/todrickhall Tyler Oakley https://www.youtube.com/tyleroakley Vsauce2 https://www.youtube.com/Vsauce2 Wassabi Productions https://www.youtube.com/hoiitsroi WereverTumorro https://www.youtube.com/werevertumorro Yuya https://www.youtube.com/lady16makeup Zoella https://www.youtube.com/zoella280390 \\u0026 more!  YouTube Rewind created by YouTube \\u0026 Portal A: http://portal-a.com Credits: http://portal-a.com/rewind2015", 'YouTube Rewind 2016. Celebrating the videos, people, music and moves that made 2016. #YouTubeRewind  Spend more time with your favorite creators, videos and trends from 2016: http://yt.be/rewind2016 Watch trending videos from 2016: http://youtube.com/rewind See trends as they happen: http://youtube.com/trending Watch the BTS video: https://youtu.be/Y8MuxHNLfZ8 Watch all the easter eggs: https://goo.gl/WihKvv  Music by The Hood Internet https://www.youtube.com/user/thehoodinternet With an original remix by Major Lazer https://www.youtube.com/user/majorlazer  Alex Wassabi https://www.youtube.com/user/hoiitsroi Alfie https://www.youtube.com/user/PointlessBlog AIB https://www.youtube.com/user/allindiabakchod AmazingPhil https://www.youtube.com/user/AmazingPhil AndreasChoice https://www.youtube.com/user/AndreasChoice Bethany Mota https://www.youtube.com/user/Macbarbie07 BFvsGF https://www.youtube.com/user/BFvsGF BibisBeautyPalace https://www.youtube.com/user/BibisBeautyPalace Bie The Ska https://www.youtube.com/user/bomberball CaELiKe https://www.youtube.com/user/CaELiKe Casey Neistat https://www.youtube.com/user/caseyneistat Caspar https://www.youtube.com/user/dicasp Connor Franta https://www.youtube.com/user/ConnorFranta Cyprien https://www.youtube.com/user/MonsieurDream danisnotonfire https://www.youtube.com/user/danisnotonfire Dude Perfect https://www.youtube.com/user/corycotton Dwayne \\"The Rock\\" Johnson https://www.youtube.com/user/therock EeOneGuy https://www.youtube.com/user/EeOneGuy elrubiusOMG https://www.youtube.com/user/elrubiusOMG enchufetv https://www.youtube.com/user/enchufetv Gigi Gorgeous https://www.youtube.com/user/GregoryGORGEOUS Grace Helbig https://www.youtube.com/user/graciehinabox hajimesyacho https://www.youtube.com/user/0214mex Hannah Hart https://www.youtube.com/user/MyHarto/ Hayla https://www.youtube.com/user/HaylaTV Hevesh5 https://www.youtube.com/user/Hevesh5 HolaSoyGerman https://www.youtube.com/user/HolaSoyGerman iHasCupquake https://www.youtube.com/user/iHasCupquake Ingrid Nilsen https://www.youtube.com/user/missglamorazzi jacksepticeye https://www.youtube.com/user/jacksepticeye Jenn McAllister https://www.youtube.com/user/jennxpenn Joey Graceffa https://www.youtube.com/user/JoeyGraceffa JoutJout Prazer https://www.youtube.com/user/joutjoutprazer KianAndJC https://www.youtube.com/user/KianAndJc KSI https://www.youtube.com/user/KSIOlajidebt Kurt Hugo Schneider https://www.youtube.com/user/KurtHugoSchneider LaurDIY https://www.youtube.com/user/LaurDIY Lilly Singh https://www.youtube.com/user/IISuperwomanII Liza Koshy https://www.youtube.com/channel/UCxSz6JVYmzVhtkraHWZC7HQ LosPolinesios https://www.youtube.com/user/LosPolinesios Luisito Rey https://www.youtube.com/user/luisitorey Luzu https://www.youtube.com/user/luzugames Mamrie Hart https://www.youtube.com/user/YouDeserveADrink Markiplier https://www.youtube.com/user/markiplierGAME Marques Brownlee https://www.youtube.com/user/marquesbrownlee MatPat https://www.youtube.com/user/MatthewPatrick13 Matt Steffanina https://www.youtube.com/user/MattSDance Meg DeAngelis https://www.youtube.com/user/maybabytumbler Meredith Foster https://www.youtube.com/user/StilaBabe09 Nicky Jam https://www.youtube.com/channel/UCpb_iJuhFe8V6rQdbNqfAlQ PewDiePie https://www.youtube.com/user/PewDiePie PIKOTARO https://www.youtube.com/channel/UCKpIOnsk-gcwHXIzuk24ExA Porta dos Fundos https://www.youtube.com/user/portadosfundos PrankvsPrank https://www.youtube.com/user/PrankvsPrank RADIO FISH https://www.youtube.com/channel/UCok3jJg7q1-PKV6XYDYTA_A Rclbeauty101 https://www.youtube.com/user/Rclbeauty101 Rhett \\u0026 Link https://www.youtube.com/user/RhettandLink Sebastián Villalobos https://www.youtube.com/user/VillalobosSebastian Seth Meyers https://www.youtube.com/user/LateNightSeth SQUEEZIE https://www.youtube.com/user/aMOODIEsqueezie sWooZie https://www.youtube.com/user/swoozie06 The Dolan Twins https://www.youtube.com/user/TheDolanTwins The Late Late Show with James Corden https://www.youtube.com/channel/UCJ0uqCI0Vqr2Rrt1HseGirg The Slow Mo Guys https://www.youtube.com/user/theslowmoguys TheWillyrex https://www.youtube.com/user/TheWillyrex Tre Melvin https://www.youtube.com/user/ThisIsACommentary Trevor Noah https://www.youtube.com/channel/UCwWhs_6x42TyRM4Wstoq8HA Unbox Therapy https://www.youtube.com/user/unboxtherapy VanossGaming https://www.youtube.com/user/VanossGaming VRZOchannel https://www.youtube.com/user/VrzoChannel Werevertumorro https://www.youtube.com/user/werevertumorro What\'s Inside? https://www.youtube.com/user/lincolnmarkham whatdafaqshow https://www.youtube.com/user/WHATDAFAQSHOW WhinderssonNunes https://www.youtube.com/user/whinderssonnunes YosStoP https://www.youtube.com/user/YosStoP Yuka Kinoshita https://www.youtube.com/user/kinoyuu0204 Yuya https://www.youtube.com/user/lady16makeup \\u0026 more!  YouTube Rewind 2016 produced by Portal A', "To celebrate 2013, we invited some YouTubers to star in a mashup of popular moments this year. Can you spot all the references? WATCH THE TOP VIDEOS OF 2013: http://yt.be/rewind  Can you name all the YouTube stars in the video? Did you get all the references to the top videos and memes of the year? (Also look for the secret, easter egg video annotations!)  #REWIND2013 Best watched in HD!  MUSIC Music remixed by DJ Earworm: http://youtube.com/djearworm  The Fox (What Does the Fox Say?) by Ylvis: http://goo.gl/Z2Q6sq Blurred Lines by Robin Thicke: http://goo.gl/8tcnhU Can't Hold Us by Macklemore \\u0026 Ryan Lewis: http://goo.gl/o1wclM Get Lucky by Daft Punk: http://goo.gl/9Z1rc1 Gentleman by PSY: http://goo.gl/X3bw7M Harlem Shake by Baauer: http://goo.gl/fOQmFX  STARRING (IN ORDER OF APPEARANCE) Kid President - http://youtube.com/soulpancake Ryan Higa - http://youtube.com/nigahiga MysteryGuitarMan - http://youtube.com/mysteryguitarman Kassem G - http://youtube.com/kassemg GloZell - http://youtube.com/glozell1 Blogilates - http://youtube.com/blogilates Kaycee Rice - http://youtube.com/brads411 I.aM.mE - http://www.youtube.com/user/IaMmECrew DeStorm - http://youtube.com/DeStorm\u200e Taryn Southern - http://youtube.com/TarynSouthern Bethany Mota - http://youtube.com/Macbarbie07  Brandon Laatsch - http://youtube.com/freddiew\u200e   Jenna Marbles - http://youtube.com/JennaMarbles\u200e   Hannah Hart - http://youtube.com/MyHarto  Rhett \\u0026 Link - http://youtube.com/RhettandLink\u200e  Tobuscus - http://youtube.com/Tobuscus\u200e  Convos With My 2-Year-Old - http://youtube.com/ConvosWith2YrOld\u200e   Alison Gold - http://youtube.com/patomuzic  Mike Tompkins - http://youtube.com/pbpproductions Epic Meal Time - http://youtube.com/EpicMealTime  Tori Locklear - http://youtube.com/vickyraye  Chester See - http://youtube.com/chestersee\u200e  Jimmy Fallon - http://youtube.com/latenight\u200e  Laina - http://youtube.com/wzr0713  Tyler Oakley - http://youtube.com/tyleroakley\u200e  Prancercise - http://youtube.com/Prancercise Quest Crew - http://www.youtube.com/user/QuestDanceCrew Girls' Generation - http://youtube.com/SMTOWN  Marina Shifrin - http://youtube.com/mvsdzb  The Fine Bros - http://youtube.com/TheFineBros\u200e  Hikakin - http://youtube.com/HIKAKIN  D-Trix - http://youtube.com/theDOMINICshow  Sam Horowitz - http://goo.gl/1U60fn Bart Baker - http://youtube.com/BartBaker Jack Hoffman - https://www.youtube.com/user/HuskerAthletics  Barely Political - http://youtube.com/barelypolitical  Alex Day - http://youtube.com/nerimon   Annoying Orange - http://youtube.com/daneboe  Dave Days - http://youtube.com/davedays Kaleb Nation - http://www.youtube.com/kalebnation Jamie Oliver - http://youtube.com/JamieOliver\u200e  iJustine - http://youtube.com/ijustine   Epic Rap Battles of History - http://youtube.com/ERB\u200e   Porta Dos Fundos - http://youtube.com/portadosfundos\u200e   Magic of Rahat - http://youtube.com/MagicofRahat\u200e   SORTED Food - http://youtube.com/sortedfood\u200e   Cookie Monster - http://youtube.com/SesameStreet  Macklemore - http://youtube.com/RyanLewisProductions  Corridor Digital - http://youtube.com/CorridorDigital The Slow Mo Guys - http://youtube.com/theslowmoguys  Smosh - http://youtube.com/smosh   Jimmy Kimmel - http://youtube.com/JimmyKimmelLive\u200e  Nick Selby - http://youtube.com/rupumped  Grace Helbig - http://youtube.com/dailygrace FreddieW - http://youtube.com/freddiew\u200e  PewDiePie - http://youtube.com/PewDiePie   ...and more!  Created by YouTube \\u0026 Portal A Full credits: http://portal-a.com/rewind  WATCH THE TOP VIDEOS OF 2013: http://yt.be/rewind WATCH THE BEHIND-THE-SCENES: http://yt.be/rewind/bts WATCH THE EFFECTS BEFORE \\u0026 AFTER: http://goo.gl/d0viKl  FEATURING AUDIO FROM: The Screaming Sheep https://youtu.be/SIaFtAKnqBU Goats Yelling Like Humans: http://youtu.be/nlYlNF30bVg Dead Giveaway by schmoyoho: http://youtu.be/nZcRU0Op5P4  The American Humane Association was present during this production. No animals were harmed in those scenes.  Inspired by Talia Joy: http://youtube.com/taliajoy18", "YouTube Rewind 2014. Celebrating the moments, memes, and people that made 2014. #YouTubeRewind  WATCH 2014’S TOP VIDS: http://yt.be/rewind WATCH THE BTS: https://youtu.be/8sPUM6QnTOI Music mixed by DJ Earworm: http://youtube.com/djearworm   BEST VIEWED IN HD!  Action Movie Kid https://youtube.com/theActionMovieKid Aichi Ono https://youtube.com/SpinboyAichi0307 Amanda Steele https://youtube.com/MakeupbyMandy24 AmazingPhil https://youtube.com/AmazingPhil Andy Raconte https://youtube.com/AndyRaconte Anil B https://youtube.com/WaRTeKGaminG Ape Crime https://youtube.com/ApeCrimeReloaded Apollos Hester http://youtu.be/X7ymriMhoj0 Barely Political https://youtube.com/barelypolitical Bart Baker https://youtube.com/BartBaKer Bethany Mota https://youtube.com/Macbarbie07 Big Bird https://youtube.com/SesameStreet Bilingirl https://youtube.com/cyoshida1231 Brett Nichols https://youtube.com/BrettNicholsOfficial Brittani Louise Taylor: https://www.youtube.com/BrittaniLouiseTaylor Carrie Fletcher https://youtube.com/ItsWayPastMyBedTime Chris Hardwick https://youtube.com/Nerdist/ Colin Furze https://youtube.com/colinfurze Conan O'Brien https://youtube.com/teamcoco Conchita Wurst https://youtube.com/ConchitaWurst Connor Franta https://youtube.com/ConnorFranta Corridor Digital https://youtube.com/CorridorDigital Cyprien https://youtube.com/MonsieurDream daaruum https://youtube.com/daaruum danisnotonfire https://youtube.com/danisnotonfire Devil Baby https://youtube.com/devilsduenyc Dodie Clark https://youtube.com/doddleoddle Ella Caney-Willis https://youtube.com/EllaSaysHiya Enjoy Phoenix https://youtube.com/EnjoyPhoenix Epic Rap Battles https://youtube.com/ERB Evan Edinger https://youtube.com/naveregnide fouseyTUBE https://youtube.com/fouseyTUBE Freddie W https://youtube.com/freddiew Gabriel Valenciano https://youtube.com/iamgabvalenciano Gal Volinez http://goo.gl/zPKRNo Grace Helbig https://youtube.com/graciehinabox Hajime https://youtube.com/0214mex Hannah Hart https://youtube.com/MyHarto Heart https://youtube.com/ThatsHeart Hello Denizen https://youtube.com/HelloDenizen Hikakin https://youtube.com/HIKAKIN HolaSoyGerman https://youtube.com/HolaSoyGerman How It Should Have Ended https://youtube.com/HISHEdotcom  IISuperwomanII https://youtube.com/IISuperwomanII iJustine https://youtube.com/ijustine   Ingrid Nilsen https://youtube.com/missglamorazzi iTakahashi https://youtube.com/iTakahashikun JennXPenn https://youtube.com/jennxpenn Jenna Marbles https://youtube.com/JennaMarbles Jimmy Kimmel https://youtube.com/JimmyKimmelLive John Oliver https://youtube.com/LastWeekTonight Kacy Catanzaro http://youtu.be/XfZFuw7a13E Kid President http://goo.gl/D9e40D Kingsley https://youtube.com/ItsKingsleyBitch Kosuke https://youtube.com/user/pazudoraya Kurt Hugo Schneider https://youtube.com/KurtHugoSchneider Le Floid https://youtube.com/LeFloid Luke Cutforth https://youtube.com/LukeIsNotSexy Mamiruton https://youtube.com/TheMaxMurai Manako (Q'ulle) http://goo.gl/EtLTpW MasuoTV https://youtube.com/MasuoTV Matt Bittner http://youtu.be/8UoJ-34Ssa0 Max Murai https://youtube.com/TheMaxMurai Michelle Phan https://youtube.com/MichellePhan Mika Shindate https://youtube.com/shindatemika Niki Albon https://youtube.com/NikiNSammy PDS https://youtube.com/PDSKabushikiGaisha Pentatonix https://youtube.com/PTXofficial PewDiePie https://youtube.com/PewDiePie PrankvsPrank https://youtube.com/PrankvsPrank Raphael Gomes https://youtube.com/ItsRaphaBlueBerry Rhett \\u0026 Link https://youtube.com/RhettandLink Rosanna Pansino https://youtube.com/RosannaPansino Sadie Miller https://youtube.com/amillerfull Sam Tsui https://youtube.com/TheSamTsui Sami Slimani https://youtube.com/HerrTutorial Sammy Albon https://youtube.com/NikiNSammy Sasaki Asahi https://youtube.com/sasakiasahi Seikin https://youtube.com/SeikinTV Sione Vaka Kelepi https://youtube.com/sionemaraschino Sir Fedora https://www.youtube.com/SirFedora SkyDoesMinecraft https://youtube.com/SkyDoesMinecraft Smosh https://youtube.com/smosh Stephen Colbert https://youtube.com/comedycentral Steve Kardynal https://youtube.com/SteveKardynal Stuart Edge https://youtube.com/stuartedge The Fine Bros https://youtube.com/TheFineBros The Gregory Brothers https://youtube.com/schmoyoho The Slow Mo Guys https://youtube.com/theslowmoguys Troye Sivan https://youtube.com/TroyeSivan18 Tyler Oakley https://youtube.com/tyleroakley VlogBrothers https://youtube.com/vlogbrothers Vsauce2 https://youtube.com/Vsauce2 Vsauce3 https://youtube.com/Vsauce3 WORLD ORDER https://youtube.com/crnaviofficial  Rewind 2014 created by YouTube \\u0026 Portal A: http://portal-a.com Full credits: http://portal-a.com/rewind2014  Special thanks to Koda, the beloved pup of Rewind's lead editor, who made her debut as Spider Dog.  Help fight ALS: http://goo.gl/aLCckj", "YouTube Rewind 2018. Celebrating the actual videos, people, music and moments that defined 2018. #YouTubeRewind SUBSCRIBE TO: FlyingKitty: https://www.youtube.com/channel/UCYQT13AtrJC0gsM1far_zJg Grandayy: https://www.youtube.com/channel/UCa6TeYZ2DlueFRne5DyAnyg Dolan Dark: https://www.youtube.com/user/BlackIceShredder Partyinbackyard: https://www.youtube.com/channel/UCIaIVpEocfuQ9fhBT1rsKrQ ____________________________________________ Extra credits: Ali A's intro: https://www.youtube.com/watch?v=u86pVtqn_kk Hit or miss: https://www.youtube.com/watch?v=3w-C0-zVaW8 Megalovania: https://tobyfox.bandcamp.com/album/undertale-soundtrack Crab rave: https://www.youtube.com/watch?v=LDU_Txk06tM", 'WATCH THE 2014 VIDEO: http://yt.be/rewind  We invited some YouTubers to star in a mash-up of culturally defining moments of 2012. Can you spot all the references?   Can you name all the YouTube stars in the video? Watch carefully and you might even find a few surprises... (Hint: try moving your mouse around in the player!).  STARRING PSY - http://youtube.com/officialpsy Walk off the Earth - http://youtube.com/walkofftheearth RyanHiga - http://youtube.com/nigahiga AlphaCat - http://youtube.com/alphacat KassemG - http://youtube.com/kassemg DailyGrace - http://youtube.com/dailygrace MysteryGuitarMan - http://youtube.com/mysteryguitarman DaveDays - http://youtube.com/davedays DeStorm - http://youtube.com/destorm PyroBooby - http://youtube.com/pyrobooby BarelyPolitical - http://youtube.com/barelypolitical RealAnnoyingOrange - http://youtube.com/realannoyingorange FreddieW - http://youtube.com/freddiew CorridorDigital - http://youtube.com/corridordigital RhettAndLink - http://youtube.com/rhettandlink Smosh - http://youtube.com/smosh FeliciaDay - http://youtube.com/geekandsundry ChesterSee - http://youtube.com/chestersee iJustine - http://youtube.com/ijustine EpicMealTime - http://youtube.com/epicmealtime MyHarto - http://youtube.com/myharto JennaMarbles - http://youtube.com/jennamarbles ShitGirlsSay - http://youtube.com/shitgirlssay JuicyStar07 - http://youtube.com/juicystar07 GloZell - http://youtube.com/glozell1 ClevverTV - http://youtube.com/clevvertv SmoshGames - http://youtube.com/smoshgames HuskyStarcraft - http://youtube.com/huskystarcraft TarynSouthern - http://youtube.com/tarynsouthern EdBassmaster - http://youtube.com/edbassmaster HeyKayli - http://youtube.com/HeyKayli CaseyLavere - http://youtube.com/caseylavere and more...  Directed by Peter Furia  Produced by Peter Furia and Beau Lewis | Director of Photography: Catherine Goldschmidt | Edited by Peter Furia and David Fine | A Seedwell Production | Full credits at http://seedwell.com/rewind', "A look into YouTube Rewind from someone who was in it. Is this what you wanted?  YouTube Rewind 2011: https://youtu.be/SmnkYyHQqNs YouTube Rewind 2012: https://youtu.be/iCkYw3cRwLo YouTube Rewind 2013: https://youtu.be/H7jtC8vjXw8 YouTube Rewind 2014: https://youtu.be/zKx2B8WCQuw YouTube Rewind 2015: https://youtu.be/KK9bwTlAvgo YouTube Rewind 2016: https://youtu.be/_GuOjXYl5ew YouTube Rewind 2017: https://youtu.be/FlsCjmMhFmw YouTube Rewind 2018: https://youtu.be/YbJOTdZBX1g  MKBHD Merch: http://shop.MKBHD.com  Video Gear I use: http://kit.com/MKBHD/video-gear#recommendation17959 Tech I'm using right now: https://www.amazon.com/shop/MKBHD  Intro Track: Half of the Way by Vulfpeck  ~ http://twitter.com/MKBHD http://snapchat.com/add/MKBHD http://google.com/+MarquesBrownlee http://instagram.com/MKBHD http://facebook.com/MKBHD", "See what the world watched on YouTube in 2011 with YouTube Rewind:\\r http://www.youtube.com/rewind\\r \\r Buy Avicii - Levels on Android Market (http://goo.gl/cO10Y) and iTunes (http://goo.gl/mYIWH).\\r \\r Re-watch the year's most viewed videos and use the interactive timeline to see the moments that defined YouTube in 2011 - the year YouTube hit one trillion views.\\r \\r Video Produced by Portal A Interactive [http://portal-a.com]\\r \\r Top 10 Most Viewed:\\r \\r Rebecca Black - Friday (OFFICIAL VIDEO) - http://youtu.be/kfVsfOSbJY0\\r Ultimate Dog Tease - http://youtu.be/nGeKSiCQkPw\\r Jack Sparrow (feat. Michael Bolton) - http://youtu.be/GI6CfKcMhjY\\r Talking Twin Babies - OFFICIAL VIDEO - http://youtu.be/_JmA2ClUvUY\\r Nyan Cat [original] - http://youtu.be/QH2-TGUlwu4\\r Look At Me Now - Chris Brown ft. Lil Wayne, Busta Rhymes (Cover by @KarminMusic) - http://youtu.be/khCokQt--l4\\r The Creep (feat. Nicki Minaj \\u0026 John Waters) - http://youtu.be/tLPZmPaHme0\\r Maria Aragon - Born This Way (Cover) by Lady Gaga\\r The Force: Volkswagen Commercial - http://youtu.be/R55e-uHQna0\\r Cat mom hugs baby kitten - http://youtu.be/Vw4KVoEVcr0", "Was 2017 amazing? Or was it just fuckall? We find out in our Desi YouTube Rewind for the year.   Don't drink and drive this new year. Book an OLA instead! Download the app here - https://goo.gl/v3MeBW  Buy our merch here -  http://www.allindiabakchod.com/merch Follow us on Instagram - https://www.instagram.com/allindiabakchod Follow us on Twitter - https://twitter.com/AllIndiaBakchod Like us on Facebook - https://www.facebook.com/IndiaBakchod Add us on snapchat - https://www.snapchat.com/add/aibofficial  Credits   Written \\u0026 Directed by Girish Narayandass  Creative Directors Girish Narayandass Devaiah Bopanna  DOP Mikhaeil Shah  Additional Writing Deepak Kumar Aakash Shah  Choreographer Melvin Louis   Assistant Choreographers Mrigakshi Jaiswal Arunima Dey Kiran Jopale  Chief AD  Kamal Dev  Associate AD’s Eeshita Chinmulgund Shubham Sharma  Production Designer Gladvin Picardo  Starring Kumar Varun Naveen Polishetty Rahul Subramaniam Rohan Joshi Ashish Shakya Shantanu Anam  Cameos Kaneez Surka Mallika Dua Zakir Khan Abish Mathew Ashish Chanchlani CarryMinati Yahya Bootwala Ranveer Allahbadia (BeerBiceps) Shahid Alvi Biswa Kalyan Rath Aadar Malik Atul Khatri  Dancers Neela Tandon Anamika Deb Chitra Jain Pranay Bafna Riya Mehendiratta Ananya Bhattacharya Aparna Reddy Dhriti Jadhav Aditya Manjrekar Chinmay Khedekar Eesha Shah Sanjay Patel Deepak Chauhan Kundan Kumar Anuja Samant  Richa Misra  Riyo Jacob Simran Jat Karan Parikh Imran Khan  Special Thanks Kenny Sebastian Bhuvan Bam BeYouNick  Music Karan Malhotra Mehar Chumble  Singers Mandar Deshpande Vidhii Upadhyay Karan Malhotra Daniel KC  Executive Producer Naveed Manakkodan  Line Producer Samkit Dagli  Editors Shashwatta Datta, Dipraj Jadhav \\u0026 Love Upadhyay  Online Editor Siddhartha Tripathi  Art Director Pankaj Rai   Second AD Yash Biyani  AIB Social Media  Aakash Shah Gladvin Picardo Deepak Kumar Sejal Badala Maseeh Ur Rahmaan  Production Executive Tejas Gaikwad  Client Servicing Nikita Sahota Jigar Seth Prerna Khatri  Finance Controller  Jay Pikle  Assistant DOP Gaurav Gokhale  Camera team Alpesh Parmar Nikhil Gulhane  Gaffer Mohammad Rafi Khan  Stylist Bhawana Vasistha  Assistant Stylist Shreya Ray  AIB Ke Dost Prateek Ramani Ashvit Bajpai Harsh Vaid Jivitesh Mazumdar Sahil Mayank Mohnish Rathod Nikhil Sahil Himanshu Joshi Rishikesh Avhad Prateek Ramani Shivam Biyani Rashi Gagrani Sehej Pahuja Vandana Riya Kapoor Annukta Ganjoo Chandani Moolchandani Khyati Padaya Ishita Kumar Akshara Sawant Saasha Balwani Esha Agarwal Muskan Mittal Nandita Shrishti Sugla Pooja Khadidkar Shalini Singh  Behind The Scenes DOP Milind Shah  Sound Recordist Rohit Pathak  Makeup and Hair Karan Singh \\u0026 Team  Camera \\u0026 Equipments 1 Stop Cine Digital  Grips  Top Gear Equipments   Lights, Grips \\u0026 Tracks Film Tools  Lightmen  Muhammed Rafi Khan \\u0026 Team  Spot Firoz \\u0026 Team  Location  Vrindavan Studios", "YouTube Rewind Compilation 2012 - 2018 A Compilation of YouTube Rewinds from the past 6 years.  T-gay shirts are available now! Now only  for 15€ Find ‘em here: https://teespring.com/shop/t-gay-shirt?tsmac=recently_viewed\\u0026tsmic=recently_viewed#pid=389\\u0026cid=102282\\u0026sid=front  DON'T CLICK THIS: https://www.youtube.com/channel/UCpOTGDMVBdzfPsrSYRXn-jQ?view_as=subscriber?sub_confirmation=1  We've chosen to not to monetize the video. (The video is claimed by the rightful music copyright owners)  List of included YouTube Rewinds: Rewind YouTube Style 2012 What Does YouTube Rewind Say 2013 Turn Down for Youtube Rewind 2014 Now Watch Me 2015 The Ultimate 2016 Challenge The Shape of 2017 Everyone Controls Rewind  YouTube Spotlight Channel: https://www.youtube.com/channel/UCBR8...  All credits can be seen on the YouTube Spotlight channel with their respective videos.  Video content shown in the video is owned and licenced to YouTube.", "It’s time to reflect on a decade of rewinds. For this list, we’re taking a look at all ten videos in the “YouTube Rewind” series, which annually recap the major events and trends of the past year. We’ll naturally be starting off with the worst of the worst, working our way up to the best of the best. And yes, we understand the irony that WatchMojo is doing a list on this particular subject. More on that later… Welcome to WatchMojo and today we’ll be ranking all the YouTube Rewinds.   This is TopX, the show where we count down the good, the bad and the ugly of YouTube.   Check out our other videos!  YouTube's 2019 Rewind: FIXED: https://www.youtube.com/watch?v=zADj2CsMCvE Top 10 YouTube Channels of 2019: https://www.youtube.com/watch?v=R7loG0uZg90 Top 10 Best TV Shows of 2019: https://www.youtube.com/watch?v=7IfrPpbcy40   Disagree with our rank? Check out the voting page for this topic and have your say!  https://www.watchmojo.com/suggest/  10. YouTube Rewind 2018: Everyone Controls Rewind 9. YouTube Rewind: The Shape of 2017 8. YouTube Rewind 2019: For the Record 7. YouTube Rewind 2010: Year in Review 6. YouTube Rewind 2011 5. YouTube Rewind: The Ultimate 2016 Challenge 4. YouTube Rewind: Turn Down for 2014 3,2,1!?!?!  Watch on WatchMojo.com  #YouTube #YouTubeRewind #Rewind2019  Check our our other channels! http://www.youtube.com/mojoplays http://www.youtube.com/mojotalks http://www.youtube.com/msmojo http://www.youtube.com/jrmojo http://www.youtube.com/watchmojouk  WatchMojo's Social Media Pages http://www.Facebook.com/WatchMojo http://www.Twitter.com/WatchMojo  http://instagram.com/watchmojo   Get WatchMojo merchandise at shop.watchmojo.com  WatchMojo’s ten thousand videos on Top 10 lists, Origins, Biographies, Tips, How To’s, Reviews, Commentary and more on Pop Culture, Celebrity, Movies, Music, TV, Film, Video Games, Politics, News, Comics, Superheroes. Your trusted authority on ranking Pop Culture.", "See what the world watched on YouTube in 2010 with YouTube Rewind: http://www.youtube.com/rewind\\r \\r Re-watch the year's most popular videos and use the interactive timeline to see the moments that defined YouTube in 2010.\\r \\r Top 10\\r #1: Bed Intruder Song - http://www.youtube.com/watch?v=hMtZfW2z9dw\\r #2: Tik Tok Kesha Parody - http://www.youtube.com/watch?v=d7n8GqewJ2M\\r #3: Greyson Chance 'Paparazzi' - http://www.youtube.com/watch?v=bxDlC7YV5is\\r #4: Annoying Orange Wazzup - http://www.youtube.com/watch?v=cL_qGMfbtAk\\r #5: The Man Your Man Could Smell Like (Old Spice)- http://www.youtube.com/watch?v=owGykVbfgUE\\r #6: Giant Double Rainbow - http://www.youtube.com/watch?v=OQSNhk5ICTI\\r #7: This Too Shall Pass OK Go - http://www.youtube.com/watch?v=qybUFnY7Y8w\\r #8: The Twilight Saga Eclipse Trailer - http://www.youtube.com/watch?v=S2HIda5wSVU\\r #9: Jimmy Surprises Bieber Fan - http://www.youtube.com/watch?v=AKEQwvaYI_k\\r #10: Gymkhana Three, Part 2 - http://www.youtube.com/watch?v=4TshFWSsrn8", "Follow Me: https://www.instagram.com/evanfong/  Listen to the outro song HERE!: https://www.youtube.com/watch?v=j2j4XKU7oMo Vanoss Spotify Playlist: https://goo.gl/rvct94 Vanoss Merch HERE!: https://vanoss.3blackdot.com/  Friends in the vid:  H2O Delirious - http://bit.ly/191aKBE Moo Snuckel - http://bit.ly/11rO5IE Panda - http://bit.ly/18Vmauu Terroriser - http://bit.ly/12YzHPL FourZer0Seven - http://bit.ly/19Z8Vqj  Follow me on Twitter - http://twitter.com/#!/VanossGaming Facebook Page - http://www.facebook.com/VanossGaming Instagram - http://instagram.com/vanossinstagram  \\r Garry's Mod map created by: https://www.linkedin.com/in/drake-rose-0408a2b6/   Please Ignore or flag spam, negative, or hateful comments.  We're here to have a good time.  Thanks everyone, and enjoy :]", "New Tsuki has launched 👘:https://tsuki.market/collections/mischief  🧎#Subscribe🧎 🥤Gfuel(affiliate): https://gfuel.ly/31Kargr #Code #Pewdiepie  ✨My Stores✨ 👕 Merch: https://represent.com/store/pewdiepie 👘 Tsuki: https://tsuki.market/ 👔 Based: https://www.based.gg 🗿 100M Figurine: https://pewdiepie.store/ 📱Customized Devices: https://rhinoshield.io/pewdiepie 👕 Terraria Collab: https://terraria.shop/collections/pewdiepie  ⚙️My Setup (affiliate link)⚙️ 🪑 Chair: https://clutchchairz.com/pewdiepie/ ⌨️ Keyboard: https://ghostkeyboards.com/pages/pewdiepie 🖱️ Mouse: https://ghostkeyboards.com/pages/pewdiepie  🕹️ Pewdiepie's Pixelings iOS: https://buff.ly/2pNG0aT Android: https://buff.ly/34C68nZ  🕹️Pewdiepie’s Tuber Simulator iOS: https://apps.apple.com/us/app/pewdiepies-tuber-simulator/id1093190533 Android: https://play.google.com/store/apps/details?id=com.outerminds.tubular\\u0026hl=en_GB\\u0026gl=US  🎮Arkade Blaster Controller: https://youtu.be/FQgLsYOKP8w Arkade Blaster Pro! #ad  ⛰️NordVPN DOWNLOAD (affiliate link)⛰️ Go to https://NordVPN.com/pewdiepie and use code PEWDIEPIE to get a 2-year plan plus 1 additional month with a huge discount. It’s risk free with Nord’s 30 day money-back guarantee!", "Grosse semaine sur Twitch entre l'escape game IRL d'Amine, Mario qui se met difficilement à la pâtisserie, des Pokémon shiny et le talent des viewers de Squeezie !  N'oublie pas le petit like sur la vidéo et abonne-toi juste ici :  https://bit.ly/youtubepopcorn (si tu actives la cloche tu es quelqu'un de bien 🤝)  🎙️ Retrouvez l'émission tous les mardis à 20h sur https://www.twitch.tv/domingo !  🎧 L'émission est également disponible en podcast ici : https://fanlink.to/b7ZX  🔥 Par ordre d'apparition 🔥 ● https://twitch.tv/JeelTV ● https://twitch.tv/aminematue ● https://twitch.tv/JLAmaru ● https://twitch.tv/Skeyma ● https://twitch.tv/lilypichu ● https://twitch.tv/AntoineDaniel ● https://twitch.tv/RayZer_Officiel ● https://twitch.tv/Kenb0gard ● https://twitch.tv/ProfessorHiro ● https://twitch.tv/JLTomy ● https://twitch.tv/Squeezie  Popcorn x RhinoShield, nouvelle collection de coques pour téléphone et AirPods disponibles ici : https://bit.ly/PopcornxRhinoShield  La boutique Popcorn : http://bit.ly/boutiquepopcorn  Nos réseaux sociaux : ● Twitter : https://bit.ly/popcorntalkshow ● Instagram : https://bit.ly/instagrampopcorn ● TikTok : https://bit.ly/tiktokpopcorn ● Facebook : https://bit.ly/facebookpopcorn  🎵 Musique du générique par : https://www.youtube.com/laekomusic  🎤 Voix off par : Thomas Deseur 🎤 Voix de l'intro : @Corobizar   Date de diffusion : 23/11/2021 - Le Rewind de Twitch  © PAB Prod"]
```

#### <a name="search_channel"></a> Get Channels by YouTube Search

###### <a name="search_channel_attributes"></a> Attributes

As with the video search you can obtain certain attributes of a channel: `id`, `info`, `valid`, `name`, `live`, `verified`, `livestream`, `livestreams`, `oldstreams`, `latest`, `playlists`, `subscribers`, `views`, `joined`, `country`, `custom_url`, `avatar`, `banner`, `description`

```py
from aiotube import *

Channel = Search.channel(keywords='SlumberDemon')

print(Channel)
print(Channel.id)
print(Channel.valid)
print(Channel.name)
print(Channel.live)
print(Channel.verified)
print(Channel.livestream)
print(Channel.livestreams)
print(Channel.oldstreams)
print(Channel.latest)
print(Channel.playlists)
print(Channel.subscribers)
print(Channel.views)
print(Channel.joined)
print(Channel.country)
print(Channel.custom_url)
print(Channel.avatar)
print(Channel.banner)
print(Channel.description)
```

Output
```
<Channel - SlumberDemon>
UCWLM2AmtzOCO68MKJn7FFuQ
True
SlumberDemon
False
False
None
None
['https://www.youtube.com/watch?v=DnvUStlvKy8', 'https://www.youtube.com/watch?v=8Or7UuuQu1Y', 'https://www.youtube.com/watch?v=eph_SIyITHw', 'https://www.youtube.com/watch?v=YGPI3qstVQo', 'https://www.youtube.com/watch?v=Vhw7Xs-EV34', 'https://www.youtube.com/watch?v=gsbAKGuy0NM', 'https://www.youtube.com/watch?v=akrS2DjUVhA', 'https://www.youtube.com/watch?v=iJh0DtCdafQ', 'https://www.youtube.com/watch?v=lK8WnMhW4IQ', 'https://www.youtube.com/watch?v=OjSvRzXNCPk', 'https://www.youtube.com/watch?v=-RG1v4gQ35I', 'https://www.youtube.com/watch?v=4uJbcSvc3L8']
<aiotube._video.Video object at 0x7f872adce9d0>
<aiotube._playlistbulk._PlaylistBulk object at 0x7f872adc0d30>
19
299
Mar 5, 2019
None
None
https://yt3.ggpht.com/4vQY7V0z0I4zNnw80YjprFSVsZIQILnVeA2WJHwW5ErW6Lqy_Vm0b1SkZ9PVo1bWOclVmIVtqdc=s176-c-k-c0x00ffffff-no-rj
https://yt3.ggpht.com/zneJ_TuExrfNuA3vpSYuPS9qoNKoxiiyOqaoPsJvfOj3NvLtYMok_2LDF23vgmZfxCmGRmp5=w1440-fcrop64=1,32b75a57cd48a5a8-k-c0xffffffff-no-nd-rj
Professional Sleepy Head
```

For channel search you can use the `info` attribute which returns a dict

```py
from aiotube import *

Channel = Search.channel('SlumberDemon')

print(Channel.info)
```

It will return the following, it includes most of the attributes above

```
{'name': 'SlumberDemon', 'id': 'UCWLM2AmtzOCO68MKJn7FFuQ', 'subscribers': '19', 'verified': False, 'views': '299', 'joined_at': 'Mar 5, 2019', 'country': None, 'url': 'https://www.youtube.com/channel/UCWLM2AmtzOCO68MKJn7FFuQ', 'custom_url': None, 'avatar_url': 'https://yt3.ggpht.com/4vQY7V0z0I4zNnw80YjprFSVsZIQILnVeA2WJHwW5ErW6Lqy_Vm0b1SkZ9PVo1bWOclVmIVtqdc=s176-c-k-c0x00ffffff-no-rj', 'banner_url': 'https://yt3.ggpht.com/zneJ_TuExrfNuA3vpSYuPS9qoNKoxiiyOqaoPsJvfOj3NvLtYMok_2LDF23vgmZfxCmGRmp5=w1440-fcrop64=1,32b75a57cd48a5a8-k-c0xffffffff-no-nd-rj'}
```

###### <a name="search_channel_uploads"></a> Uploads

You can also get a channels uploads, you can limit the amount of uploads being returned. The amount of uploads being returned can vary, depending on the channel.

```py
from aiotube import *

Channel = Search.channel('SlumberDemon')

Uploads = Channel.uploads(limit=100)

print(Uploads)
```

Output:

```
<aiotube._videobulk._VideoBulk object at 0x7f79d4c38be0>
```

This will output a **videobulk** object which also as the atributes: `ids`, `urls`, `views`, `likes`, `dislikes`(This property is deprecated as YouTube is slowly removing public dislike counts), `durations`, `dates`, `parents`, `descriptions`, `thumbnails`, `tags`

```py
from aiotube import *

Channel = Search.channel('SlumberDemon')

Uploads = Channel.uploads(limit=100)

print(Uploads.ids)

# I will stop listing all atributes as they are listed above
```

Output:

```
['DnvUStlvKy8', '8Or7UuuQu1Y', 'eph_SIyITHw', 'YGPI3qstVQo', 'Vhw7Xs-EV34', 'gsbAKGuy0NM', 'akrS2DjUVhA', 'iJh0DtCdafQ', 'lK8WnMhW4IQ', 'OjSvRzXNCPk', '-RG1v4gQ35I', '4uJbcSvc3L8']
```

###### <a name="search_channel_bulk"></a> Bulk

Channel search also has a **channelbulk** similar to the **videobulk**, it also has attributes: `ids`, `urls`, `names`, `subscribers`, `views`, `joined`, `countries`, `custom_urls`, `descriptions`, `avatars`, `banners`, `verifieds`, `lives`

```py
from aiotube import *

Channels = Search.channels('SlumberDemon', limit=100)

print(Channels.urls)
```

Output:

```
['https://www.youtube.com/channel/UCWLM2AmtzOCO68MKJn7FFuQ', 'https://www.youtube.com/channel/UCx1PWgmfWcqWVxYBRM8q94A', 'https://www.youtube.com/channel/UCWtZi-HxIi0jr5_kRohjzDg', 'https://www.youtube.com/channel/UCis1VaiFEeATtO1pR8GPQmg', 'https://www.youtube.com/channel/UCI5kni1RjFHrf_yRoauMygA', 'https://www.youtube.com/channel/UCSgTtERNeZCrhbLnO5G7xxg', 'https://www.youtube.com/channel/UCNOJIP1vP0d0LwLX4WmysRw', 'https://www.youtube.com/channel/UCYIYHWS80rTKOxkkYkKWPeQ']
```

#### <a name="search_playlist"></a> Get Playlist by YouTube Search

###### <a name="search_playlist_attributes"></a> Attributes

Aiotube can also get a youtube playlist you can also use attributes: `name`, `url`, `video`, `videos`, `video_count`, `thumbnail`

```py
from aiotube import *

Playlist = Search.playlist("youtube rewind")

print(Playlist.name)
print(Playlist.url)
```

Output:

```
Youtube Rewind (2010-2020)
https://www.youtube.com/playlist?list=PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD
```

You can also use the `info` attribute to get more data in one attribute

```py
from aiotube import *

Playlist = Search.playlist("youtube rewind")

print(Playlist.info)
```

This returns a dict with the follwoing:

```
{'name': 'Youtube Rewind (2010-2020)', 'video_count': '11', 'videos': ['UFnXm6cjGwU', 'SmnkYyHQqNs', 'iCkYw3cRwLo', 'H7jtC8vjXw8', 'zKx2B8WCQuw', 'KK9bwTlAvgo', '_GuOjXYl5ew', 'FlsCjmMhFmw', 'YbJOTdZBX1g', '2lAe1cqCOXo', 'PKtnafFtfEo'], 'thumbnail': 'https://i.ytimg.com/vi/_GuOjXYl5ew/hqdefault.jpg', 'url': 'https://www.youtube.com/playlist?list=PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD'}
```

###### <a name="search_playlist_bulk"></a> Bulk

Getting playlists in bulk. The attributes are: `urls`, `names`, `video_counts`, `thumbnails`

```py
from aiotube import *

Playlists = Search.playlists("youtube rewind", limit=100)

print(Playlists.urls)
```

This outputs the following:

```
['https://www.youtube.com/playlist?list=PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD', 'https://www.youtube.com/playlist?list=PLx-c0UVUWu65y8_EGEo_Lks4mxKOumKxF', 'https://www.youtube.com/playlist?list=PLhdPK-ltXSXs8jRhGMNGe83pU6rqaIeN7', 'https://www.youtube.com/playlist?list=PLgMZtDLLgvm5RcNpoGyJD26DLNGY_pUHU', 'https://www.youtube.com/playlist?list=PLTkfy1XLdfRW48neIqa6csHJxrGhnefMZ', 'https://www.youtube.com/playlist?list=PLEXxpZnZ4AIRtYYJ9NHstzFFATldpzV4O', 'https://www.youtube.com/playlist?list=PL7bFK8nXNg45LGCnEXkhxvciRSFjfJVMy', 'https://www.youtube.com/playlist?list=PLP5PFxCytZR9oaJcKLpT4wHLFzKZiTcRN', 'https://www.youtube.com/playlist?list=PLSTz8jpJdr5qbDTyWb1bTQOe9B9sL7trD', 'https://www.youtube.com/playlist?list=PL_vkVwrwck3PXHB4OtBjbyG9DH12NmJk1', 'https://www.youtube.com/playlist?list=PLvfIP1A1djX3_x8LMYKsj8t0YoATcQ4Qo', 'https://www.youtube.com/playlist?list=PLVhwJgrZ2diwXdEnB203c7glSVm-82rFi', 'https://www.youtube.com/playlist?list=PLkhDNPPThDa8HA5Ni3jYV2O1wQCgu45FS', 'https://www.youtube.com/playlist?list=PLdmaVVZzw1Y8FAbtOKe8t05R77kfTyqbO', 'https://www.youtube.com/playlist?list=PLKUm8k0QsdKlqdTeJW5fl-xUR0EOsnwUJ', 'https://www.youtube.com/playlist?list=PL3htSLmnUpaNAmReR7x5yUslVJWXH5KQw', 'https://www.youtube.com/playlist?list=PLlb8F9Jx9j37oO0UCWdfNbFcJ3tXikzN7', 'https://www.youtube.com/playlist?list=PLXe5am-H8n59uoU8oZGl1I3Br2f_hgBCI', 'https://www.youtube.com/playlist?list=PLaSF6TE2yo0q_m5W3e6Mf0As34UuH0qDk', 'https://www.youtube.com/playlist?list=PLOexZ_eIttCc4Us4yBoWlSv_KzI4VrIUv']
```

## <a name="video"></a> Create an instance of Video Data

#### <a name="video_basics"></a> Basics

With aiotube you can get info on spesific videos instead of finding them through search. You will always need to add attributes or aiotube will only return an `object`

```py
from aiotube import *

Vid = Video("8Or7UuuQu1Y&t=6s") # video Id / video url

print(Vid)
```

This will give you the following video object:

```
<aiotube._video.Video object at 0x7fa2d8198b80>
```

#### <a name="video_attributes"></a> Attributes

To get info on the video we can use attributes: `title`, `views`, `likes`, `dislikes`(This property is deprecated as YouTube is slowly removing public dislike counts), `author`, `duration`, `url`, `thumbnail`, `tags`

```py
from aiotube import *

Vid = Video("8Or7UuuQu1Y&t=6s") # video Id / video url

print(Vid.title)
print(Vid.url)
print(Vid.author)
```

This outputs the following:

```
LEGO Builder's Journey Part 5
https://www.youtube.com/watch?v=8Or7UuuQu1Y&t=6s
UCWLM2AmtzOCO68MKJn7FFuQ
```

#### <a name="video_dict"></a> Dict

You can also get data by using the `info` attribute which returns a dict

```py
from aiotube import *

Vid = Video("8Or7UuuQu1Y&t=6s") # video Id / video url

print(Vid.info)
```

Output:

```
{'title': "LEGO Builder's Journey Part 5", 'id': '8Or7UuuQu1Y&t=6s', 'views': '18', 'likes': '4', 'duration': '0h 18m 43s', 'author': 'SlumberDemon', 'uploaded': '2021-09-04', 'url': 'https://www.youtube.com/watch?v=8Or7UuuQu1Y&t=6s', 'thumbnail': 'https://i.ytimg.com/vi/8Or7UuuQu1Y/maxresdefault.jpg', 'tags': ['video', ' sharing', ' camera phone', ' video phone', ' free', ' upload']}
```

## <a name="channel"></a> Create an instance of YouTube Channel

#### <a name="channel_attributes"></a> Attributes

Similar to the [video basics](#video_basics) if you don't include any attributes it will return an `object`. To get channel data you can use the following attributes: `id`, `valid`, `name` `info`(Returns dict), `live`, `verified`, `livestream`, `livestreams`, `oldstreams`, `latest`, `playlists`, `subscribers`, `views`, `joined`, `country`, `custom_url`, `avatar`, `banner`, `description`

```py
from aiotube import *

Channel = Channel("UCWLM2AmtzOCO68MKJn7FFuQ") # channel Id / url / custom url

print(Channel.url)
print(Channel.name)
```

Output:

```
https://www.youtube.com/channel/UCWLM2AmtzOCO68MKJn7FFuQ
SlumberDemon
````

## <a name="playlist"></a> Create an instance of Playlist Data

#### <a name="playlist_attributes"></a> Attributes

To get playlist data we can use the following attributes: `info`(Returns dict), `name`, `url`, `video_count`, `thumbnail`

```py
from aiotube import *

Playlist = Playlist("PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD") # playlist id

print(Playlist.name)
print(Playlist.url)
print(Playlist.video_count)
```

Output:

```
Youtube Rewind (2010-2020)
https://www.youtube.com/playlist?list=PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD
11
```

You can also use the `videos` attribute, which retuns `video` objects. Currently you can't do anything with them but in future there will be a selection of attributes to use.

```py
from aiotube import *

Playlist = Playlist("PLBnetXbvs5BGzGIsoxe6MYhX1hB7iRoOD") # playlist id

Videos = Playlist.videos(limit=100)

print(Videos)
```

Output:

```
[<aiotube._video.Video object at 0x7f0ac724bc70>, <aiotube._video.Video object at 0x7f0ac724bdc0>, <aiotube._video.Video object at 0x7f0ac724bc10>, <aiotube._video.Video object at 0x7f0ac724bcd0>, <aiotube._video.Video object at 0x7f0ac724bd00>, <aiotube._video.Video object at 0x7f0ac724bf40>, <aiotube._video.Video object at 0x7f0ac724bfa0>, <aiotube._video.Video object at 0x7f0ac7259850>, <aiotube._video.Video object at 0x7f0ac7259100>, <aiotube._video.Video object at 0x7f0ac72598e0>, <aiotube._video.Video object at 0x7f0ac7259070>]
```

## <a name="extras"></a> Create an instance of YouTube Extras

#### <a name="extras_attributes"></a> Attributes

Using extras alows you to get the currently trending videos. The following attributes can be used: `trending`, `music`, `gaming`, `news`, `livestream`, `learning`, `sports`

```py
from aiotube import *

Extras = Extras()

print(Extras.trending)
print(Extras.music)
print(Extras.gaming)
print(Extras.news)
print(Extras.livestream)
print(Extras.learning)
print(Extras.sports)
```

This will output the following:

```
<aiotube._video.Video object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
<aiotube._videobulk._VideoBulk object at 0x7fccb009cfa0>
```

Extras will return [video](#video_attributes) and [VideoBulk](#search_video_bulk) objects. These links will lead to the attributes that can be used to obtain more information from these objects. An example can be seen below:

```py
from aiotube import *

Extras = Extras()

print(Extras.trending.url) # single video object in url format
print(Extras.music.urls) # multiple video bulk objects in url format
```

Output:

```
https://www.youtube.com/watch?v=2jfbXZiE6Lc
['https://www.youtube.com/watch?v=-AxZDTPX5x8', 'https://www.youtube.com/watch?v=PfwIpoVMvNs', 'https://www.youtube.com/watch?v=waADh9bESBk', 'https://www.youtube.com/watch?v=8e7S8l4s1OM', 'https://www.youtube.com/watch?v=4zqsbsWttcI', 'https://www.youtube.com/watch?v=1qrhnK6FGr0', 'https://www.youtube.com/watch?v=cw1qDzyiYW4', 'https://www.youtube.com/watch?v=fmKrSGTfCiU', 'https://www.youtube.com/watch?v=idqomUhHrQE', 'https://www.youtube.com/watch?v=fUWcVNLNvrs', 'https://www.youtube.com/watch?v=aAkMkVFwAoo', 'https://www.youtube.com/watch?v=B-tOZxoNrFk', 'https://www.youtube.com/watch?v=wKhRnZZ0cJI', 'https://www.youtube.com/watch?v=_JmwTmhC3zg', 'https://www.youtube.com/watch?v=_p0PjkdLFm4', 'https://www.youtube.com/watch?v=oMCG-fL-uCM', 'https://www.youtube.com/watch?v=2xttF0lM_Wk', 'https://www.youtube.com/watch?v=Ew-zmk81G1k', 'https://www.youtube.com/watch?v=PhKVSZsRxQM', 'https://www.youtube.com/watch?v=GyBlCur-eJ0', 'https://www.youtube.com/watch?v=a3U_Oeezy18', 'https://www.youtube.com/watch?v=KWTLVZMBhBY', 'https://www.youtube.com/watch?v=MdNfV0667C8', 'https://www.youtube.com/watch?v=58g_dyMTQHQ', 'https://www.youtube.com/watch?v=KyA8f5E4q8w', 'https://www.youtube.com/watch?v=__6OB8_QZC8', 'https://www.youtube.com/watch?v=PWU3MapYLMw', 'https://www.youtube.com/watch?v=rSEd7vZo6Lk', 'https://www.youtube.com/watch?v=IL_UlIcuYMc', 'https://www.youtube.com/watch?v=2iaA5NxC69E', 'https://www.youtube.com/watch?v=0U5CWjQeUnE', 'https://www.youtube.com/watch?v=uPD0QOGTmMI', 'https://www.youtube.com/watch?v=GChxzIwyNt4', 'https://www.youtube.com/watch?v=JJwEoHmteZE', 'https://www.youtube.com/watch?v=kSl8EwMrwjE', 'https://www.youtube.com/watch?v=zc372PmNIzE', 'https://www.youtube.com/watch?v=0dje_eehMIE', 'https://www.youtube.com/watch?v=hz_pTf76Suk', 'https://www.youtube.com/watch?v=XYnMAnZTQu0', 'https://www.youtube.com/watch?v=_64VTQLdFGQ', 'https://www.youtube.com/watch?v=39NfSiXXgcE', 'https://www.youtube.com/watch?v=nPwCmfgJl30', 'https://www.youtube.com/watch?v=nrIPxlFzDi0', 'https://www.youtube.com/watch?v=5qm8PH4xAss', 'https://www.youtube.com/watch?v=ViwtNLUqkMY', 'https://www.youtube.com/watch?v=eBG7P-K-r1Y', 'https://www.youtube.com/watch?v=d05tQrhNMkA', 'https://www.youtube.com/watch?v=LfRNRymrv9k', 'https://www.youtube.com/watch?v=_JZom_gVfuw', 'https://www.youtube.com/watch?v=gJLIiF15wjQ', 'https://www.youtube.com/watch?v=4N1iwQxiHrs', 'https://www.youtube.com/watch?v=hSofzQURQDk', 'https://www.youtube.com/watch?v=Lrle0x_DHBM', 'https://www.youtube.com/watch?v=eVTXPUF4Oz4', 'https://www.youtube.com/watch?v=35AWgksymtA', 'https://www.youtube.com/watch?v=kTJczUoc26U', 'https://www.youtube.com/watch?v=e4ujS1er1r0', 'https://www.youtube.com/watch?v=tqiXwx0NG0Q', 'https://www.youtube.com/watch?v=Jf3JOkPsogI', 'https://www.youtube.com/watch?v=-dB7P2kRJ8Q', 'https://www.youtube.com/watch?v=_NGQfFCFUn4', 'https://www.youtube.com/watch?v=O1Qh7j1yD8Y', 'https://www.youtube.com/watch?v=UJtjoQ5TcVI', 'https://www.youtube.com/watch?v=FTQbiNvZqaY', 'https://www.youtube.com/watch?v=orJSJGHjBLI', 'https://www.youtube.com/watch?v=nAUwKeO93bY', 'https://www.youtube.com/watch?v=ffcitRgiNDs', 'https://www.youtube.com/watch?v=ngG2XKJ_y1Q', 'https://www.youtube.com/watch?v=jx0Ag3fEeDE', 'https://www.youtube.com/watch?v=nJr_8l0AEWE', 'https://www.youtube.com/watch?v=TfJf9T8f9u4', 'https://www.youtube.com/watch?v=H-OJFUU0lyE', 'https://www.youtube.com/watch?v=gpzmn4ZoB5k', 'https://www.youtube.com/watch?v=mHrQXY93qMc', 'https://www.youtube.com/watch?v=sCX2Uc75_T4', 'https://www.youtube.com/watch?v=4ymUUTvAkkc', 'https://www.youtube.com/watch?v=BK78W5t5YlI', 'https://www.youtube.com/watch?v=U3ASj1L6_sY', 'https://www.youtube.com/watch?v=U2SNwtE-0Us', 'https://www.youtube.com/watch?v=tollGa3S0o8', 'https://www.youtube.com/watch?v=eeNv4wf2D1U', 'https://www.youtube.com/watch?v=ksY3wb4vtlA', 'https://www.youtube.com/watch?v=y8trd3gjJt0', 'https://www.youtube.com/watch?v=G_zuB-ogIBw', 'https://www.youtube.com/watch?v=0Gjx-ZQuQ_Y', 'https://www.youtube.com/watch?v=agvibm7Wqy4', 'https://www.youtube.com/watch?v=nzGVO6BR4Ek', 'https://www.youtube.com/watch?v=HZ8V7HpkAtk', 'https://www.youtube.com/watch?v=NC4bc0OFvwk', 'https://www.youtube.com/watch?v=5isjqo_xtCo', 'https://www.youtube.com/watch?v=2F34hoIEFkk', 'https://www.youtube.com/watch?v=faf98cNY8A8', 'https://www.youtube.com/watch?v=zNv46Vp-l18', 'https://www.youtube.com/watch?v=H0ciir6G0jA', 'https://www.youtube.com/watch?v=eQvj5LRacrM', 'https://www.youtube.com/watch?v=FPLTf_3-FP0', 'https://www.youtube.com/watch?v=VwPZ58WGcrs', 'https://www.youtube.com/watch?v=g450xDoMxKo', 'https://www.youtube.com/watch?v=snsTmi9N9Gs', 'https://www.youtube.com/watch?v=U5rLz5AZBIA', 'https://www.youtube.com/watch?v=OMHHUsQRmvo', 'https://www.youtube.com/watch?v=7xzU9Qqdqww', 'https://www.youtube.com/watch?v=a_YR4dKArgo', 'https://www.youtube.com/watch?v=DUT5rEU6pqM', 'https://www.youtube.com/watch?v=bqpA5Acc8-c', 'https://www.youtube.com/watch?v=GtUVQei3nX4', 'https://www.youtube.com/watch?v=oUbpGmR1-QM', 'https://www.youtube.com/watch?v=vYMxOzxKYYo', 'https://www.youtube.com/watch?v=iWyvMerss4w', 'https://www.youtube.com/watch?v=0DdCoNbbRvQ', 'https://www.youtube.com/watch?v=y7394ESN91Y', 'https://www.youtube.com/watch?v=J4_W-R3iPJ8']
```

## <a name="end"></a> The end

Thank you for reading this long guide! If you have any problems or ideas join the [`Support Server(Discord)`](https://discord.gg/YAFGAaMrTC) or comment on this gist! 

Written by [SlumberDemon](slumberdemon.carrd.co)
