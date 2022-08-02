from processing import Processing
from onlyvideo import Only_video
from playwright.sync_api import sync_playwright
from re import search

class Str_tok_tik(Processing, Only_video):

    def __init__(self, file_type, url, trim=None, pitch=None, velocity=None):
        self.url = url
        super().__init__(trim, pitch, velocity)
        Only_video.__init__(self, *self.get_urls(), file_type)
    
    def get_urls(self):
        with sync_playwright() as playwright:
            chromium = playwright.chromium
            browser = chromium.launch(channel="chrome")
            page = browser.new_page()
            page.set_extra_http_headers({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"})
            page.goto(self.url)
            page.inner_html("video")
            content = page.content()
            title = page.title()
        re = r"<video.+src=\"(.+)\"></video>"    
        real_url = search(re, content).group(1)
        real_url = real_url.replace("amp;", "")
        for i in "\/:*¿\"<>|-\'()?.":
            title = title.replace(i, "")
        return f"{title}.mp4", real_url

    def download(self):
        super().download()
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