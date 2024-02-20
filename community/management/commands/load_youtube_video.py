from django.core.management import BaseCommand
from googleapiclient.discovery import build
from django.conf import settings
from rest_framework.exceptions import ValidationError

from community.domain.definition import PLAYLIST_ID_KEY_CATEGORY_VALUE
from community.serializers import LectureCreateSerializer
from edumax_account.model.user_access import get_user_with_pk


class Command(BaseCommand):
    help = 'db에 youtube로 부터 동영상들의 id를 load 한다'

    def handle(self, *args, **kwargs):
        self.load_youtube_video_id()

    def load_youtube_video_id(self):
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        next_page_token = None
        print("_________________________________________________________________________")
        print("youtube로 부터 video id load를 시작합니다.")
        print("_________________________________________________________________________")
        for playlist_id, category_list in PLAYLIST_ID_KEY_CATEGORY_VALUE.items():
            print(f"<<<<playlist_id:{playlist_id}>>>>")
            while True:
                playlist_items_request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=50,  # 리소스 요청 최대 개수
                    pageToken=next_page_token
                )
                playlist_items_response = playlist_items_request.execute()

                category_depth_1 = category_list[0]
                category_depth_2 = category_list[1]
                category_depth_3 = category_list[2]
                category_depth_4 = category_list[3]
                for item in playlist_items_response['items']:

                    video_id = item['snippet']['resourceId']['videoId']
                    title = item['snippet']['title']
                    admin_user = get_user_with_pk(1)  # 우선 관리자가 올리는걸로..

                    serializer_data = {
                        "youtube_id": video_id,
                        "title": title,
                        "author": admin_user.id,
                        "category_d1": category_depth_1,
                        "category_d2": category_depth_2,
                        "category_d3": category_depth_3,
                        "category_d4": category_depth_4
                    }
                    print("title:", title, "playlist_id:", playlist_id)
                    serializer = LectureCreateSerializer(data=serializer_data)

                    if not serializer.is_valid():
                        raise ValidationError(serializer.errors)

                    serializer.save()

                # 다음페이지가 있는지 확인
                next_page_token = playlist_items_response.get('nextPageToken')
                if not next_page_token:
                    break
