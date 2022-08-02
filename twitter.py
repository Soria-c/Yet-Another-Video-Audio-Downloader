from processing import Processing
from m3u8_m4s_ts import M3u8_m4s_ts
from playwright.sync_api import sync_playwright


class Twitter(Processing, M3u8_m4s_ts):
    
    def __init__(self, file_type, url, trim=None, pitch=None, velocity=None):
        self.url = url
        self.base_url = "https://video.twimg.com"
        super().__init__(trim, pitch, velocity)
        M3u8_m4s_ts.__init__(self, *self.get_urls(), file_type)

    def get_urls(self):
        with sync_playwright() as playwright:
            net = []
            chromium = playwright.chromium
            browser = chromium.launch(channel="chrome")
            page = browser.new_page()
            page.set_extra_http_headers({"user-agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"})
            page.on("response", lambda response: net.append(f"{response.header_value('content-type')} {response.request.url}"))
            page.goto(self.url, wait_until="networkidle")
            title = page.title()
        container = list(filter(lambda x: "application/x-mpegURL" in x, net))[0].split()[1]
        #print(init)
        #print(container)
        for i in "\/:*¿\"<>|-\'()?.":
            title = title.replace(i, "")
        title = title.encode("ascii", "ignore")
        title = title.decode()
        #print(title)
        return f"asd.mp4", container
    
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
            container_url: {self.container_url}
            filename: {self.filename}
        """