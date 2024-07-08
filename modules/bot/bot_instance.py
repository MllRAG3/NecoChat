from pyrogram import Client
from os import environ
from typing import Final
from dotenv import load_dotenv

load_dotenv()

Il: Final[Client] = Client(
    environ['name'],
    api_id=environ["api_id"], api_hash=environ['api_hash'],
    bot_token=environ['bot_token']
)
