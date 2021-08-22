import re
import aiohttp
import asyncio


URL = 'https://www.youtube.com/channel/CHANNEL_ID' # Replace Channel ID

async def get_channel_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            raw_data = await resp.text()
            data = re.findall(r"\"text\":\" (\S{8})", raw_data)
            if data[0] == 'watching':
                VideoIDList = re.findall(r"watch\?v=(\S{11})",raw_data) # List of video ids of all livestreams
                url = f'https://www.youtube.com/watch?v={VideoIDList[0]}' # URL of first YouTube Livestream
                print(url)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_channel_data(URL))
