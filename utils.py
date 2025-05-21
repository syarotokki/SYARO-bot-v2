import requests
import os

# 環境変数からYouTube APIキーを取得
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def fetch_latest_video(channel_id):
    """
    指定されたYouTubeチャンネルの最新動画1件を取得する
    """
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

def fetch_past_videos(channel_id, max_results=10):
    """
    指定されたYouTubeチャンネルの過去の動画を最大max_results件取得する
    """
    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?key={YOUTUBE_API_KEY}"
            f"&channelId={channel_id}"
            f"&part=snippet"
            f"&order=date"
            f"&maxResults={max_results}"
            f"&type=video"
        )
        response = requests.get(url)
        data = response.json()

        if "items" not in data or not data["items"]:
            return []

        videos = []
        for item in data["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                "video_id": video_id,
                "title": title,
                "url": video_url
            })

        return videos

    except Exception as e:
        print(f"[ERROR] fetch_past_videos: {e}")
        return []

    except Exception as e:
        print(f"[ERROR] fetch_latest_video: {e}")
        return None
