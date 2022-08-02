from playwright.sync_api import sync_playwright
from processing import Processing
from video_audio import Video_audio
import os
import subprocess

class Facebook(Processing, Video_audio):

    def __init__(self, file_type, url, trim=None, pitch=None, velocity=None):
        self.url = url
        super().__init__(trim, pitch, velocity)
        Video_audio.__init__(self, file_type, *self.get_urls())

    def get_urls(self):
        with sync_playwright() as playwright:
            net = []
            chromium = playwright.chromium
            browser = chromium.launch(channel="chrome")
            page = browser.new_page()
            page.on("response", lambda response: net.append(f"{response.header_value('content-type')} {response.request.url}"))
            page.set_extra_http_headers({"User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"})
            page.goto(self.url, wait_until="networkidle")
            result = page.title().split(" | Facebook")[0]

        net2 = list(filter(lambda x: "video/mp4" in x , net))
        net3 = list(filter(lambda x: "video/webm" in x, net))

        if not(net3):
            #print(net2)
            #print(net3)
            net4 = list(set([i.split()[1].split("&bytestart")[0] for i in net2]))
            video_url = net4[0]
            format_video = ".mp4"
            audio_url = net4[1]
            format_audio = format_video
        else:
            video_url = net3[0].split()[1].split("&bytestart")[0]
            audio_url = net2[0].split()[1].split("&bytestart")[0]
            format_audio = ".mp4"
            format_video = ".webm"


        for i in "\/:*¿\"<>|-\'()?.":
            result = result.replace(i, "")
        return f"audio{result}{format_audio}", audio_url, f"noaudio{result}{format_video}",  video_url
    
    def download(self):
        super().download()
        if self.file_type == "audio":
            cmd = ["ffprobe", "-i", self.video_filename, "-show_streams", "-select_streams", "a", "-loglevel", "error"]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            c = 0
            for _ in iter(p.stdout.readline, b''):
                c += 1
                break
            if not(c):
                os.remove(self.video_filename)
                final_name = self.audio_filename[5:]
                os.rename(self.audio_filename, final_name)
            else:
                os.remove(self.audio_filename)
                final_name = self.audio_filename[7:]
                os.rename(self.video_filename, final_name)
            self.filename = final_name
        else:
            self.merge_files()
        self.trim_file()
        self.transpose()
        self.change_velocity()

