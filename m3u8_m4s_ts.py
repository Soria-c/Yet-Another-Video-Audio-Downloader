import requests
from re import search
import m3u8
from onlyvideo import Only_video
from async_dl import download_all
import asyncio
import os
import subprocess
import sys
from tqdm import tqdm

class M3u8_m4s_ts:

    def __init__(self, filename, container_url, file_type):
        self.filename = filename
        self.container_url = container_url
        self.file_type = file_type
    
    def download(self):
        cls_name = self.__class__.__name__
        container = requests.get(self.container_url)
        
        playlist = self.base_url + m3u8.loads(container.text).data['playlists'][0]['uri']
        
        
        playlist_info = requests.get(playlist).text
        init_mp4 = search( r"URI=\"(.+)\"", playlist_info)
        if (init_mp4):
            init_mp4 = self.base_url + init_mp4.group(1)
        segments = m3u8.loads(playlist_info).data['segments']
        
        if (cls_name == "Twitter"):
            files = [f"{self.base_url}{i['uri']}" for i in segments]
            pbar2 = tqdm(total=len(files), unit='B', unit_scale=True)
            with open(self.filename, "wb") as f:
                if (init_mp4):
                    f.write(requests.get(init_mp4).content)
                    pbar2.update(1)
                for i in files:
                    data = requests.get(i)
                    f.write(data.content)
                    pbar2.update(1)
        else:
            if (cls_name == "Twitch"):
                self.base_url = playlist.replace(playlist.split("/")[5], "")
                files = [[f"{self.base_url}{i['uri']}", i['uri']] for i in segments]

            elif (cls_name == "Daily_Motion"):
                self.base_url = f"https://{playlist.split('/')[2]}"
                files = [[f"{self.base_url}{i['uri']}", f"{i['uri'].split('/')[2].replace('(', '').replace(')', '')}.ts"] for i in segments]

            with open("files.txt", "w") as f:
                for i in files:
                    f.write(f"file \'{i[1]}\'")
                    f.write("\n")
            while(files):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(download_all(files))
                files = list(filter(lambda x: not os.path.exists(x[1]), files))

            cmd = ["ffmpeg", "-f", "concat", "-i", "files.txt", "-c", "copy", f"{self.filename}"]
            subprocess.run(cmd)
            with open("files.txt", "r") as f:
                f.seek(0)
                fs = f.readlines()
                #print(fs)
                for i in fs:
                    fd = i[:-1].split("\'")[1]
                    if os.path.exists(fd):    
                        os.remove(fd)
            os.remove("files.txt")
       
        if self.file_type == "audio":
            Only_video.only_get_audio(self.filename)
