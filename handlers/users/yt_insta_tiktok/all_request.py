import os

import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
INSTAGRAM_HOST = os.getenv("RAPIDAPI_INSTAGRAM_HOST")
TIKTOK_HOST = os.getenv("RAPIDAPI_TIKTOK_HOST")
YOUTUBE_HOST = os.getenv("RAPIDAPI_YOUTUBE_HOST")


def _headers(host):
    return {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": host,
    }


## instagram
def instagram(link):
    url = f"https://{INSTAGRAM_HOST}/index"
    querystring = {"url": {link}}

    response = requests.request("GET", url, headers=_headers(INSTAGRAM_HOST), params=querystring)
    media = response.json()
    video = media['media']
    return video


# tiktok
def tiktok(link):
    url = f"https://{TIKTOK_HOST}/"
    querystring = {"url": {link}, "hd": "0"}

    response = requests.request("GET", url, headers=_headers(TIKTOK_HOST), params=querystring)
    media: dict = response.json()
    data: dict = media.get('data')
    video = data.get('play')
    return video


def you_tube(link):
    url = f"https://{YOUTUBE_HOST}/v2/video/details"
    querystring = {"videoId": f"{link}"}

    response = requests.request("GET", url, headers=_headers(YOUTUBE_HOST), params=querystring)
    media: dict = response.json()
    data: dict = media.get("videos")
    title = media.get("title")
    video_file: dict = data.get("items")[1]
    video = video_file.get("url")
    return title, video
