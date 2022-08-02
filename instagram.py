from re import search
from processing import Processing
from onlyvideo import Only_video
from deep_insta_login import login
import requests

username = ""
password = ""

class Instagram(Processing, Only_video):

    def __init__(self, file_type, url=None, target=None, trim=None, pitch=None, velocity=None):  
        self.url = url
        self.target = target
        if (self.url):
            #r = requests.get(self.url)
            #re = search(r"\(&#\d+;(.+)\) &#x\d+;", r.text)
            self.target = self.url.split('/')[5]
            
        super().__init__(trim, pitch, velocity)
        Only_video.__init__(self, *self.get_urls(file_type), file_type)

    def get_urls(self, file_type):
        api = login(username, password)
        user_id = api.username_info(self.target)['user']['pk']
        if (file_type == "stories"):  
            s = api.user_reel_media(str(user_id))
            urls = []
            count = 0
            for i in s['items']:
                if i["media_type"] == 1:
                    url = i['image_versions2']['candidates'][0]['url']
                    urls.append([url, f"{self.target}_{count}.jpg"])
                elif i["media_type"] == 2:
                    url2 = i['video_versions'][0]['url']
                    urls.append([url2, f"{self.target}_{count}.mp4"])
                count += 1
            return "", urls
        result = api.user_feed(str(user_id))
        code = self.url.split('/')[4]
        data = result['items']
        next_max_id = result.get('next_max_id')
        while next_max_id:
            for i in data:
                if i['code'] == code:
                    return f"{self.target}_video_{code}.mp4", i['video_versions'][0]['url']
            results = api.user_feed(str(str(user_id)), max_id=next_max_id)
            data = results['items']
            next_max_id = results.get('next_max_id')

    def download(self):
        super().download()
        if (self.file_type != "stories"):
            self.trim_file()
            self.transpose()
            self.change_velocity()

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
