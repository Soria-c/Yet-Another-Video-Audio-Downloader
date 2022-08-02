import subprocess
import os
import requests
from tqdm import tqdm
import asyncio
from async_dl import download_all
import queue


class Only_video:

    def __init__(self, filename, url, file_type):
        self.filename = filename
        self.real_url = url
        self.file_type = file_type
    

    def download(self):
        if (self.file_type == "stories"):
            failed = []
            loop = asyncio.get_event_loop()
            loop.run_until_complete(download_all(self.real_url, failed))            
            if (failed):
                for i in failed:
                    if (".jpg" in i[1]):
                        h = 'x-full-image-content-length'
                    else:
                        h = 'Content-Length'
                    r = requests.get(i[0])
                    pbar = tqdm(total=int(r.headers[h]), unit='B', unit_scale=True)
                    with open(i[1], "wb") as f:
                        for j in r.iter_content(chunk_size=8196):
                            f.write(j)
                            pbar.update(len(j))
            return
        data = requests.get(self.real_url, stream=True)
        pbar2 = tqdm(total=int(data.headers["Content-Length"]), unit='B', unit_scale=True)
        with open(self.filename, "wb") as f:
            for i in data.iter_content(chunk_size=8196):
                f.write(i)
                pbar2.update(len(i))
        if self.file_type == "audio":
            self.only_get_audio(self.filename)

    @staticmethod
    def only_get_audio(filename):
        cmd = ["ffmpeg", "-i", filename, "-vn", "-acodec", "copy", f"a{filename}"]
        subprocess.call(cmd)
        os.remove(filename)
        os.rename(f"a{filename}", filename)