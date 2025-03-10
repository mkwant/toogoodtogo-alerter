import os
from pathlib import Path

import humanize
from dateutil import parser as date_parser
from rich import print
from tgtg import TgtgClient

from src.Alerter.alerter import Alerter, TelegramAlerter
from src.Serializer.serializer import JsonSerializer
from src.TooGoodToGo.client import get_client


# TODO Serialize offer item id (json or pickle), read back.
# TODO Telegram parse mode https://core.telegram.org/bots/api#formatting-options

def tgtg_alert(client: TgtgClient, alerter: Alerter):
    for offer in client.get_items():

        if offer['items_available']:
            pickup_interval = offer['pickup_interval']
            pickup_day = humanize.naturalday(date_parser.parse(pickup_interval['start']))
            pickup_start = date_parser.parse(pickup_interval['start']).strftime(format='%H:%M')
            pickup_end = date_parser.parse(pickup_interval['end']).strftime(format='%H:%M')
            msg = f"<b>{offer['display_name']}</b>\n" \
                  f"<blockquote>offer['item']['description']</blockquote>\n" \
                  f"{pickup_day} {pickup_start} - {pickup_end} <i>({offer['items_available']} left)</i>"

            alerter.send_msg(msg=msg)


def main():
    client = get_client(email_address=os.getenv('TGTG_EMAIL_ADDRESS'))
    alerter = TelegramAlerter(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'), chat_id=os.getenv('TELEGRAM_CHAT_ID'))
    tgtg_alert(client=client, alerter=alerter)


def test_telegram():
    alerter = TelegramAlerter(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'), chat_id=os.getenv('TELEGRAM_CHAT_ID'))
    msg = f"<b>TestMaarten</b>\n" \
          f"<blockquote>Omschrijving beschrijving verhaal hoop tekst. Wat een hoop woorden, echt een hele lap. " \
          f"Blabla bla het gaat maar door.</blockquote>\n" \
          f"tomorrow 12.00 - 13.00 <i>(3 left)</i>\n"
    alerter.send_msg(msg=msg)


def test_serializer():
    serializer = JsonSerializer(Path('tgtg_alert_history.json'))
    res = serializer.check_id_exists('456')
    print(res)


if __name__ == '__main__':
    # main()
    # test_telegram()
    test_serializer()