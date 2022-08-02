#from playwright.sync_api import sync_playwright
from re import search
from processing import Processing
from onlyvideo import Only_video
#import subprocess
from pytube import YouTube
#import os
from sys import exit


class Youtube(Processing, Only_video):
    
    def __init__(self, file_type, url, trim=None, pitch=None, velocity=None):
        self.url = url
        super().__init__(trim, pitch, velocity)
        Only_video.__init__(self, *self.get_urls(), file_type)

    def get_urls(self):
        
        #Had to use pytube instead for faster downloads
        yt = YouTube(self.url)
        urls = [i['url'] for i in yt.streaming_data['formats']]
        q = {int(search(r'itag=(.*)&source', j).group(1)): j for j in urls}
        l = sorted([i for i in q.keys()], reverse=True)
        title = yt.title
        for i in "\/:*¿\"<>|-\'()?.":
            title = title.replace(i, "")
        return  f"{title}.mp4", q[l[0]]
        """ with sync_playwright() as playwright:
            net = []
            chromium = playwright.chromium
            browser = chromium.launch(channel="chrome")
            page = browser.new_page()
            l2 = 0
            l3 = 0
            while((l2 and not l3) or (l3 and not l2) or (not l2 and not l3)):
                net = []
                page.on("response", lambda response: net.append(f"{response.header_value('content-type')} {response.request.url}"))
                page.goto(self.url)
                net2 = list(filter(lambda x: "audio/webm" in x , net))
                l2 = len(net2)
                net3 = list(filter(lambda x: "video/mp4" in x, net))
                if (not net3):
                    net3 = list(filter(lambda x: "video/webm" in x, net))
                l3 = len(net3)
                if (l2 < 1 or l3 < 1):
                    continue
                durs_v = {str(int(float(search(r'dur=(.*)&lmt', j.split()[1]).group(1)))): j.split()[1] for j in net3}
                durs_a = {str(int(float(search(r'dur=(.*)&lmt', i.split()[1]).group(1)))): i.split()[1] for i in net2}

                l = sorted([int(i) for i in durs_a.keys()], reverse=True)
                print(l)
                ll = sorted([int(j) for j in durs_v.keys()], reverse=True)

                print(ll)
                #print(net3)
                print(l2, l3)
                if (abs(l[0] - ll[0]) > 20):
                    l2 = 0
                    l3 = 0
                    continue
            result = page.title().split(" - YouTube")[0]
        video_url = durs_v[str(ll[0])].split("&range")[0]
        audio_url = durs_a[str(l[0])].split("&range")[0]
        format_audio = net2[0].split()[0].split("/")[1]
        format_video = net3[0].split()[0].split("/")[1]
        
        for i in "\/:*¿\"<>|-\'()?.":
            result = result.replace(i, "")
        print(f"{result}")
        if (file_type == "audio"):
            return f"audio{result}.{format_audio}", audio_url
        if (file_type == "video"):
            return f"audio{result}.{format_audio}", audio_url, f"noaudio{result}.{format_video}",  video_url """
        

    
    def download(self):
        super().download()
        self.trim_file()
        self.transpose()
        self.change_velocity()
        """ if (search(r"^.*\.webm$", self.audio_filename)):
            new_name = f"{self.audio_filename[5:len(self.audio_filename) - 5]}.mp3"
            cmd = ["ffmpeg", "-i", self.audio_filename, new_name]
            subprocess.call(cmd)
            os.remove(self.audio_filename)
            self.audio_filename = new_name
            self.filename = new_name
        if self.file_type == "video":
            self.merge_files() """

    def __repr__(self):
        return f"""
            class: {self.__class__.__name__}
            file_type: {self.file_type}
            url: {self.url}
            trim: {self.trim}
            pitch: {self.pitch}
            velocity: {self.velocity}
            real_url: {self.real_url}
            filename: {self.filename}
        """
    

