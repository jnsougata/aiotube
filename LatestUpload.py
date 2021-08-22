import re
import aiohttp
import asyncio

CHANNELID = 'UCU9FEimjiOV3zN_5kujbCMQ'           # Replace channel id

async def get_channel_data(ID:str):
    url = f'https://www.youtube.com/channel/{ID}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            raw_data = await resp.text()
            isLive = re.findall(r"\"text\":\" (\S{8})", raw_data)
            if isLive[0] != 'watching':
                QUERY = f'{url}/videos'
                async with session.get(QUERY) as data:
                    raw_data = await data.text()
                    NEW_DATA = re.findall(r"watch\?v=(\S{11})",raw_data)
                    print(NEW_DATA)                # Prints a list of latest video ids
            else:
                print('Channel is currently live now!')          # Don't work while channel is live



loop = asyncio.get_event_loop()
loop.run_until_complete(get_channel_data(CHANNELID))
