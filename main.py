#!/usr/bin/python

from sys import argv, exit
from re import search
from youtube import Youtube
from facebook import Facebook
from instagram import Instagram
from twitter import Twitter
from tiktok import Str_tok_tik
from twitch import Twitch
from daily_motion import Daily_Motion
from colorama import Fore, Back, Style


def main(kwargs):
    # basic regex
    yt = r"https://(www.youtube.com/(watch\?v=|shorts/)|youtu.be/)(.{10}|.{11})$"
    fb = r"https://(www.facebook.com/(watch/?\?v=|.+/videos/|reel/)\d{15,17}(/|/\?s=ifu)?$|fb.watch/\w{10}/?$)"
    ig = r"(https://www.instagram.com/(p|tv|reel)/.{11}/?(\?utm_source=ig_web_copy_link)?|^(?!https://).{0,30}$)"
    tw = r"https://twitter.com/.+/status/(\d{19})$"
    str_tok = r"https://www.tiktok.com/.+/video/\d{19}\?(is_copy_url=1&)?is_from_webapp=v?1(&sender_device=pc&web_id=\d{19})?"
    twt = r"https://www.twitch.tv/videos/\d{1,10}"
    dm = r"https://www.dailymotion.com/video/.{7}(\?playlist=x5nmbq)?"
    
    sources = {
        "youtube":{
            "re":yt,
            "class": Youtube
        },
        "facebook":{
            "re": fb,
            "class": Facebook
        },
        "instagram":{
            "re": ig,
            "class": Instagram
        },
        "twitter":{
            "re": tw,
            "class": Twitter
        },
        "tiktok":{
            "re": str_tok,
            "class": Str_tok_tik
        },        
        "twitch":{
            "re": twt,
            "class": Twitch
        },
        "daily_motion":{
            "re": dm,
            "class": Daily_Motion
        }
    
    }
    #print(kwargs["url"])
    if "url" in kwargs:
        src = kwargs["url"]
    else:
        src = kwargs["target"]
    print("Procesando...")
    for v in sources.values():
        if (search(v["re"], src)):
            if (kwargs['file_type'] == 'stories' and v["class"].__name__ != 'Instagram'):
                print("Stories only supported for instagram")
                exit(1)
            source = v["class"](**kwargs)
            print(source)
            print("Descargando")
            source.download()
            print(source)
            print_banner()
            print("Descarga completada")
            exit(0)
    print("Invalid url")
    
def print_usage():
    
    print(Fore.GREEN + Style.BRIGHT + """Usage: pydl <video|audio|stories> <url> [-t|v|p] [hh:mm:ss-hh:mm:ss] [xN] [t:tr]
    Options:
    
        -t          trim, range: [hh:mm:ss-hh:mm:ss]
        -v          velocity: [xN], where 'N' is a number
        -p          pitch: [t:tr], where 't' is the temperament and 'tr' is the transpose interval('semitone')

    Examples:
        pydl audio <url> -v x2
        pydl video <url> -pv 12:5 x1.5
        pydl video <url> -vpt x1.2 13:3 00:01:30-00:02:00
        pydl <video|audio> https://www.instagram.com/p|tv|reel/<code>/<username> (Please add the uploader username at the end)
        pydl stories <ig_username>""")
    exit()

def print_banner():
    print(Fore.LIGHTBLUE_EX  + """
▓█████▄  ▒█████   █     █░███▄    █  ██▓     ▒█████   ▄▄▄      ▓█████▄ ▓█████  ██▀███  
▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░██ ▀█   █ ▓██▒    ▒██▒  ██▒▒████▄    ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
░██   █▌▒██░  ██▒▒█░ █ ░█▓██  ▀█ ██▒▒██░    ▒██░  ██▒▒██  ▀█▄  ░██   █▌▒███   ▓██ ░▄█ ▒
░▓█▄   ▌▒██   ██░░█░ █ ░█▓██▒  ▐▌██▒▒██░    ▒██   ██░░██▄▄▄▄██ ░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
░▒████▓ ░ ████▓▒░░░██▒██▓▒██░   ▓██░░██████▒░ ████▓▒░ ▓█   ▓██▒░▒████▓ ░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒ ░ ▒░   ▒ ▒ ░ ▒░▓  ░░ ▒░▒░▒░  ▒▒   ▓▒█░ ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░ ░ ░░   ░ ▒░░ ░ ▒  ░  ░ ▒ ▒░   ▒   ▒▒ ░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░ ░ ░ ░ ▒    ░   ░    ░   ░ ░   ░ ░   ░ ░ ░ ▒    ░   ▒    ░ ░  ░    ░     ░░   ░ 
   ░        ░ ░      ░            ░     ░  ░    ░ ░        ░  ░   ░       ░  ░   ░     
 ░                                                              ░   

Download Audio/Video from: Youtube, Facebook, Twitter, Twitch, Daily Motion and Instagram(login required)
Developed by Soria.c""")
    print(Style.RESET_ALL)
if __name__ == "__main__":
    print_banner()
    del argv[0]
    l = len(argv)
    if (l < 2):
        print_usage()
    if (argv[0] not in ['audio', 'video', 'stories']):
        print_usage()
    kwargs = {
        "file_type": argv[0],
        "url": argv[1]
    }
    if (argv[0] == "stories"):
        kwargs['target'] = kwargs.pop('url')
    if (l > 2):
        re = r"^-([v?t?p?]{1,3})$"
        r = search(re, argv[2])
        if (not r):
            print_usage()
        ops = r.group(1)
        if (len(set(ops)) != len(ops)):
            print_usage()
        kwops = {
            "t": ["trim", r"^((?:\d\d:?){2}\d\d)-((?:\d\d:?){2}\d\d)$"], 
            "v": ["velocity", r"^x\d(?:.\d)?$"],
            "p": ["pitch", r"^\d+:-?\d+$"]
        }
        for i in argv[3:]:
            for j in ops:
                if search(kwops[j][1], i):
                    kwargs.update({kwops[j][0]:i})
    main(kwargs)
