import os

import humanize
from dateutil import parser as date_parser
from rich import print
from tgtg import TgtgClient

from src.Alerter.alerter import Alerter, TelegramAlerter
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
            msg = f"- {offer['display_name']} -\n" \
                  f"[{offer['item']['item_id']}] ({offer['items_available']} left)\n" \
                  f"{pickup_day} {pickup_start} - {pickup_end}"
            print(offer['item']['description'])
            print(offer['item']['cover_picture']['current_url'])

            alerter.send_msg(msg=msg)


def main():
    client = get_client(email_address=os.getenv('TGTG_EMAIL_ADDRESS'))
    alerter = TelegramAlerter(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'), chat_id=os.getenv('TELEGRAM_CHAT_ID'))
    tgtg_alert(client=client, alerter=alerter)


def test_telegram():
    alerter = TelegramAlerter(bot_token=os.getenv('TELEGRAM_BOT_TOKEN'), chat_id=os.getenv('TELEGRAM_CHAT_ID'))
    msg = f"TestMaarten\n" \
          f"[123] (3 left)\n" \
          f"tomorrow 12.00 - 13.00"
    alerter.send_msg(msg=msg)


if __name__ == '__main__':
    test_telegram()
