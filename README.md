Usage:
pydl <video|audio|stories> <url> [-t|v|p] [hh:mm:ss-hh:mm:ss] [xN] [t:tr]
    Options:
    
        -t          trim, range: [hh:mm:ss-hh:mm:ss]
        -v          velocity: [xN], where 'N' is a number
        -p          pitch: [t:tr], where 't' is the temperament and 'tr' is the transpose interval('semitone')

    Examples:
        pydl audio <url> -v x2
        pydl video <url> -pv 12:5 x1.5
        pydl video <url> -vpt x1.2 13:3 00:01:30-00:02:00
        pydl <video|audio> https://www.instagram.com/p|tv|reel/<code>/<username> (Please add the uploader username at the end)
        pydl stories <ig_username>
