import asyncio
import aiohttp
from tqdm import tqdm


async def download_all(urls, failed=None):
    my_conn = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=my_conn) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_link(url=url, session=session, failed=failed))
            tasks.append(task)
        await asyncio.gather(*tasks,return_exceptions=True)


async def download_link(url, session, failed):
    headers = {}
    if (".jpg" in url[1]):
        h = 'x-full-image-content-length'
    else:
        h = 'Content-Length'
    
    #if "source=youtube&" in url[0]:
    #    headers = {
    #        "Accept": "*/*",
    #        "Connection": "keep-alive",
    #        "Range": "bytes=0-",
    #        "Referer": url[0],
    #        "Sec-Fetch-Dest": "video",
    #        "Sec-Fetch-Mode": "no-cors",
    #        "Sec-Fetch-Site": "same-origin",
    #        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    #}

    async with session.get(url[0]) as response:
        
        if int(response.status) != 200:
            failed.append(url)
            return
        pbar2 = tqdm(total=int(response.headers[h]), unit='B', unit_scale=True)
        with open(url[1], "wb") as f2:
            async for chunk2 in response.content.iter_chunked(8196):
                    f2.write(chunk2)
                    pbar2.update(len(chunk2))
    
