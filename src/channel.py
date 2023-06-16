import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        custom_url = channel['items'][0]['snippet']['customUrl']
        self.url = f'https://www.youtube.com/{custom_url}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, filename):
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': f'{self.description}',
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        '''
        получить данные о канале по его id
        docs: https://developers.google.com/youtube/v3/docs/channels/list

        сервис для быстрого получения id канала: https://commentpicker.com/youtube-channel-id.php
        '''
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)
