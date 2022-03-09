import os
import spotipy
import spotipy.oauth2 as oauth2
import yt_dlp
from pytube import YouTube
from youtube_search import YoutubeSearch
import io

def find_and_download_song(title: str) -> io.BytesIO:
    buffer = io.BytesIO()
    best_url = None
    try:
        results_list = YoutubeSearch(title, max_results=10).to_dict()
        best_url = f"https://www.youtube.com{results_list[0]['url_suffix']}"
    except IndexError:
        return Exception
    url_ = YouTube(best_url)
    sounds = url_.streams.filter(only_audio=True)
    used_sounds = []
    for sound in sounds[::-1]:
        if sound.abr not in used_sounds:
            used_sounds.append(sound.abr)
            if sound.filesize < 50000000:
                size = f"Downloading song in {sound.abr} ({round(float(sound.filesize / 1000000), 2)} MB)"
                sound_ = sound
                break
    
    itag = sound_.itag
    sound = url_.streams.get_by_itag(itag)
    sound.stream_to_buffer(buffer)
    buffer.seek(0)

    return buffer, size