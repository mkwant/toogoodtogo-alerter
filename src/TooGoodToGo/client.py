import json
from pathlib import Path

import dotenv
from tgtg import TgtgClient

# Load environment variables
dotenv.load_dotenv()


def get_credentials(email_address: str) -> None:
    client = TgtgClient(email=email_address)
    credentials = client.get_credentials()
    with open('../tgtg_creds.json', 'w') as f:
        json.dump(credentials, f, indent=4)


def get_client(email_address: str) -> TgtgClient:
    json_file = Path('tgtg_creds.json')
    if not json_file.is_file():
        get_credentials(email_address=email_address)
    credentials = json.load(json_file.open())

    return TgtgClient(
        access_token=credentials['access_token'],
        refresh_token=credentials['refresh_token'],
        user_id=credentials['user_id'],
        cookie=credentials['cookie']
    )
