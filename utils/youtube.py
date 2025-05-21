import requests
import os
from datetime import datetime, timezone

def fetch_latest_video(channel_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"

    response = requests.get(url)
    if response.status_code != 200:
        return None

    items = response.json().get("items", [])
    if not items:
        return None

    video = items[0]
    is_live = video["snippet"].get("liveBroadcastContent") == "live"
    video_id = video["id"].get("videoId")
    published_at = video["snippet"]["publishedAt"]
    published_ts = int(datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())

    return {
        "title": video["snippet"]["title"],
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "is_live": is_live,
        "published_at_ts": published_ts
    }
