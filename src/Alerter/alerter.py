import os
from abc import ABC

import requests


class Alerter(ABC):
    def send_msg(self, msg) -> bool:
        raise NotImplementedError


class TelegramAlerter(Alerter):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    @classmethod
    def from_env(cls):
        return cls(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
                   chat_id=os.getenv('TELEGRAM_CHAT_ID'))

    def send_msg(self, msg: str) -> bool:
        # msg = PlainText(msg).to_markdown()
        print(msg)

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': msg,
            'parse_mode': 'HTML'
        }

        print(url)
        r = requests.get(url, params=params)
        print(r.status_code)
        print(r.content)
        return r.ok
