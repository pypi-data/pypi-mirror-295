import yt_dlp
from youtubesearchpython import Search
from datetime import datetime
import os
import subprocess
import pydub
from pydub import AudioSegment
import random
def download(video_url,path):

    path_to_vid = path + '%(title)s.%(ext)s'


    ydl_opts = {'format' : 'mp4',
                'outtmpl': path_to_vid}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    return path_to_vid

def find_link(query,lim,num):
    allsearch = Search(query, limit =lim)
    result = allsearch.result()
    links = []
    for i in range(num):
        links.append(result['result'][i]['link'])

    return links

def download_all(query, no_of_vids,path,num):
    links = find_link(query,no_of_vids,num)

    path = os.path.join(path,str(random.random()))
    os.mkdir(path)

    for link in links:
        download(link,path)
    print(path)
    return path

def mashup(query,no_of_videos,duration,out_path):
    path_to_videos = download_all(query,no_of_videos,out_path,no_of_videos)
    
    duration_for_each = int(duration/no_of_videos)
    path_to_audios = os.path.join(path_to_videos,"audio")
    os.mkdir(path_to_audios)
    i = 0
    for vid in os.listdir(path_to_videos):
        path_to_video = os.path.join(path_to_videos[0:-5],vid)
        print("\n\n",path_to_video)
        # vid = "C:\Projects\Machine-Learning-UCT513\Mashup_package/video.webm"
        out_path = os.path.join(path_to_audios,str(i)+".mp3")
        subprocess.run(['ffmpeg', '-i', path_to_video, out_path], check=True)
        i+=1
        
        audios = []
    for audio in os.listdir(path_to_audios):
        path_to_audio = os.path.join(path_to_audios,audio)
        current_song = AudioSegment.from_file(path_to_audio)
        start_time = 0 # Start time (30 seconds)
        end_time = duration_for_each*1000   # End time (60 seconds)
        cropped_audio = audio[start_time:end_time]
        cropped_audio.export(path_to_audio, format="mp3")
        audios.append(path_to_audio)
    combined_audio = AudioSegment.from_file(audios[0])
    for file in audios[1:]:
        audio = AudioSegment.from_file(file)
        combined_audio += audio
        
    combined_audio.export(out_path, format='mp3')
