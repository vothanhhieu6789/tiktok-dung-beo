import asyncio
import json
from pathlib import Path

import aiofiles
import aiohttp

with open('data.json', 'r') as f:
    search_results = json.loads(f.read())


# %%
async def get_pokemon(session, url, folder, created, format):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'video',
        'Referer': url,
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Range': 'bytes=0-'
    }
    async with session.get(url, headers=headers) as resp:
        Path(f'download/{folder}').mkdir(exist_ok=True)
        video_file = await aiofiles.open(f'download/{folder}/{created}.{format}', mode='wb+')
        await video_file.write(await resp.read())
        await video_file.close()
        return 'ok'


async def downloader(user_data):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video in user_data:
            video_url = video['video']['downloadAddr']
            folder = video['author']['uniqueId']
            created = video['createTime']
            format = video['video']['format']
            tasks.append(asyncio.ensure_future(get_pokemon(session, video_url, folder, created, format)))

        await asyncio.gather(*tasks)


asyncio.run(downloader(search_results))
