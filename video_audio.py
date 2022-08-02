import asyncio
from async_dl import download_all
import subprocess
import os

class Video_audio:

    def __init__(self, file_type, audio_filename, audio_url, video_filename=None, video_url=None):
        self.audio_filename = audio_filename
        self.video_filename = video_filename
        self.audio_url = audio_url
        self.video_url = video_url
        self.file_type = file_type
        self.filename = None

    def download(self):
        if (self.video_filename):
            urls = [[self.audio_url, self.audio_filename], [self.video_url, self.video_filename]]
        else:
            urls = [[self.audio_url, self.audio_filename]]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all(urls))
    
    def merge_files(self):
            final_name = f"{self.video_filename[7:-5]}.mp4"
            cmd = ["ffmpeg", "-i", self.video_filename, "-i", self.audio_filename, "-c:v", "copy", "-c:a", "aac", final_name]
            subprocess.call(cmd)
            os.remove(f"{self.video_filename}")
            os.remove(f"{self.audio_filename}")
            self.filename = final_name

    def __repr__(self):
        return f"""
            class: {self.__class__.__name__}
            file_type: {self.file_type}
            url: {self.url}
            trim: {self.trim}
            pitch: {self.pitch}
            velocity: {self.velocity}
            video_url: {self.video_url}
            audio_url: {self.audio_url}
            filename: {self.filename}
        """
