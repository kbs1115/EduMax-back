from celery import shared_task
from googleapiclient.discovery import build
from django.conf import settings
from model.models import Lecture


@shared_task
def fetch_and_save_video_id(search_query):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    request = playlist_items_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # Max allowed by API
            pageToken=next_page_token
        )

    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        # Lecture.objects.create(video_id=video_id)
