from pytube import YouTube, Playlist
from urllib.error import HTTPError

"""
Handle HTTP 403 Errors: YouTube might block requests for certain formats or resolutions.You could try different itag values or catch
the error and retry with a different resolution
"""
def download_video(url, resolution):
    try:
        video = YouTube(url)
        stream = get_stream_by_resolution(video, resolution)
        if stream:
            stream.download()
            return stream.default_filename
        else:
            print(f"Stream not available for resolution {resolution}. Trying lower resolution.")
            return download_video(url, "low")
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return None

def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)

def download_playlist(url, resolution):
    playlist = Playlist(url)
    download_videos(playlist.video_urls, resolution)

def get_stream_by_resolution(video, resolution):
    if resolution in ["low", "360", "360p"]:
        stream = video.streams.filter(res="360p", file_extension="mp4").first()
    elif resolution in ["medium", "720", "720p", "hd"]:
        stream = video.streams.filter(res="720p", file_extension="mp4").first()
    elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        stream = video.streams.filter(res="1080p", file_extension="mp4").first()
    elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        stream = video.streams.filter(res="2160p", file_extension="mp4").first()
    else:
        stream = video.streams.filter(res="360p", file_extension="mp4").first()

    return stream

def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link.lower() != "stop":
        link = input()
        if link.lower() != "stop":
            links.append(link)

    return links
