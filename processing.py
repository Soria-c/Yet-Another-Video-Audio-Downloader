import subprocess
import os

class Processing():
    def __init__(self, trim, pitch, velocity):
        self.trim = trim
        self.pitch = pitch
        self.velocity = velocity

    def trim_file(self):
        if (self.trim):
            start, end = self.trim.split("-")
            cmd = ["ffmpeg", "-i", self.filename, "-ss", start, "-to", end, "-c:v", "copy", "-c:a", "copy", "a" + self.filename]
            subprocess.run(cmd)
            self.remove_temp()
    
    def transpose(self):
        if (self.pitch):
            t, tr = self.pitch.split(":")
            interval = 2 ** (int(tr)/int(t))
            cmd = ["ffmpeg", "-i", self.filename, "-filter:a", f'rubberband=pitch={interval}', "a" + self.filename]
            subprocess.run(cmd)
            self.remove_temp()
    
    def change_velocity(self):
        if (self.velocity):
            t = float(self.velocity.split('x')[1])
            if (self.file_type == "video"):
                v = 1 / t
                cmd = ["ffmpeg", "-i", f"{self.filename}", "-filter_complex", f"[0:v]setpts={v}*PTS[v];[0:a]rubberband=tempo={t}[a]", "-map", "[v]", "-map", "[a]", f"a{self.filename}"]
            else:
                cmd = ["ffmpeg", "-i", f"{self.filename}", "-filter:a", f"rubberband=tempo={t}", f"a{self.filename}"]
            subprocess.run(cmd)
            self.remove_temp()
    
    def remove_temp(self):
        os.remove(self.filename)
        os.rename(f"a{self.filename}", self.filename)
