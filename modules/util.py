import datetime

from modules.database.models import models, Users, Chats, ChatUsers
from modules.database import db
from modules.config import OP_USERS

from peewee import DoesNotExist
from pyrogram.types import User, Chat

import re


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


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


class UserManager:
    def __init__(self, user: User, chat: Chat):
        self.user: User = user
        self.chat: Chat = chat

    @property
    def from_database(self) -> Users:
        try:
            return Users.get(id_in_telegram=self.user.id)
        except DoesNotExist:
            data = {
                "id_in_telegram": self.user.id,
                "custom_name": self.user.first_name,
                "admin_rights_lvl": int(self.user.id in OP_USERS)
            }
            db_user = Users.create(**data)
            data = {
                "chat": ChatManager(self.chat).from_database,
                "member": self.from_database
            }
            ChatUsers.create(**data)

            return db_user

    @property
    def default_permissions(self) -> dict[str, bool]:
        db_user = self.from_database
        return {
            "can_send_messages": db_user.can_send_messages,
            "can_send_media_messages": db_user.can_send_media_messages,
            "can_send_other_messages": db_user.can_send_other_messages,
            "can_send_polls": db_user.can_send_polls,
            "can_add_web_page_previews": db_user.can_add_web_page_previews,
            "can_change_info": db_user.can_change_info,
            "can_invite_users": db_user.can_invite_users,
            "can_pin_messages": db_user.can_pin_messages,
        }

    @staticmethod
    def save(new):
        Users.save(new)


def is_command(text: str) -> bool:
    if text is None: return False
    return text.startswith('/')


def extract_arguments(text: str) -> str or None:
    regexp = re.compile(r"/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
    result = regexp.match(text)
    return result.group(2) if is_command(text) else None


def safe_to_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None


def safe_to_datetime(value: str, f: str = "%d/%m/%Y %H:%M") -> datetime.datetime | None:
    try:
        return datetime.datetime.strptime(value, f)
    except ValueError:
        return None


zero_datetime = datetime.datetime(day=1, month=1, year=1, hour=0, minute=0, second=0, microsecond=0)
