from fastapi import FastAPI
from googleapiclient.discovery import build
import random
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

# using the api key from the Youtube Data API v3 credentials
API_KEY = os.environ.get("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)



app = FastAPI()
# fixing blocked by cors policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with the appropriate origins
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/videodetails")
def random_video():
    try:
        # Search for YouTube videos
        request = youtube.search().list(
            part="snippet",
            type="video",
            order="viewCount",  # Sort videos by view count
            maxResults=50,
            regionCode="US", 
            #videoCategoryId=20
        )
        response = request.execute()
        video_items = response["items"]

        #choosing a random youtube video from the the videos fetched
        random_video = random.choice(video_items)
        video_id = random_video["id"]["videoId"]
        video_title = random_video["snippet"]["title"]

        # Statistics of the fetched youtube vid
        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        stats_response = stats_request.execute()
        video_stats = stats_response["items"][0]["statistics"]
        video_views = video_stats["viewCount"]

        return {
            "title": video_title,
            "views": video_views,
            "video_id": video_id
        }
    except Exception as e:
        return {"error":str(e)}
