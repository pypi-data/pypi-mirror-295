import requests
from scrapeanything.database.repository import Repository
from scrapeanything.utils.config import Config
from scrapeanything.utils.api_service import ApiService

class TelegramBot:

    def __init__(self, config: Config) -> None:
        self.TOKEN = config.get(section='NOTIFIERS', key='TELEGRAM_CHATID')
        self.CHAT_ID = config.get(section='NOTIFIERS', key='TELEGRAM_TOKEN')

    def get_chat_id(self) -> str:
        url = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"
        print(requests.get(url).json())

    def send_message(self, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={message}"
        print(requests.get(url).json()) # this sends the message

    def send_image(self, filename: str, caption: str=None) -> None:
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendPhoto'
        files = {'photo': open(f'{filename}.png', 'rb')}
        data = {'chat_id': self.CHAT_ID, 'caption': caption }
        print(requests.post(url, files=files, data=data))