from pyrogram.types import Chat
from modules.database.models import Chats

from peewee import DoesNotExist


class ChatManager:
    def __init__(self, chat: Chat):
        self.chat: Chat = chat

    @property
    def from_database(self) -> Chats:
        try:
            return Chats.get(id_in_telegram=self.chat.id)
        except DoesNotExist:
            data = {
                "id_in_telegram": self.chat.id,
                "custom_title": self.chat.title,
            }
            return Chats.create(**data)
