from pytube import YouTube 

def find_video(link):
    try:
        yt=YouTube(link)
        output= {
        'title':yt.title,
        'thumbnail':yt.thumbnail_url,
        'channel':yt.channel_id
        }
        return output
    except:
        return 0

def download_video(link,reso,path):
    try:
        yt=YouTube(link)
    except:
        return 0
    if reso==1:
        video=yt.streams.get_highest_resolution()
        video.download(path)
        return
    else:
        video=yt.streams.get_lowest_resolution()
        video.download(path)
        return
    
def download_audio(link,path):
    try:
        yt=YouTube(link)
        audio=yt.streams.get_audio_only()
        audio.download(path)
        return
    except:
        return 0
    


       