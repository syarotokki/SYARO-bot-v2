import requests
import os

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def fetch_latest_video(channel_id):
    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?key={YOUTUBE_API_KEY}"
            f"&channelId={channel_id}"
            f"&part=snippet"
            f"&order=date"
            f"&maxResults=1"
            f"&type=video"
        )
        response = requests.get(url)
        data = response.json()

        if "items" not in data or not data["items"]:
            return None

        item = data["items"][0]
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        return {
            "video_id": video_id,
            "title": title,
            "url": video_url
        }

    except Exception as e:
        print(f"[ERROR] fetch_latest_video: {e}")
        return None
