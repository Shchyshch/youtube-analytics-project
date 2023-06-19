import isodate
import datetime
from src.channel import youtube
from src.video import Video


class PlayList:
    def __init__(self, playlist_id):
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        self.playlist_id = playlist_id
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails'
        ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

    @property
    def total_duration(self):
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()

        duration = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = duration + isodate.parse_duration(iso_8601_duration)

        return duration

    def show_best_video(self):
        max_likes = 0
        best_vid_url = ''
        for video in self.video_ids:
            vid = Video(video)
            if int(vid.like_count) > max_likes:
                max_likes = int(vid.like_count)
                best_vid_url = vid.url
        return best_vid_url
