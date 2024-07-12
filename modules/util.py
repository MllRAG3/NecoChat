from modules.config import OP_USERS
from modules.database.models import models, ChatMembers, ChatMemberSettings, Chats, Users
from modules.database import db
from modules.errors import LowArgs

from pyrogram.types import Message, Chat, User
from datetime import datetime
import re
import json


class JsonConverter:
    def __init__(self, obj):
        self.obj = obj
        self.type = str(type(obj))

    @property
    def json(self) -> str:
        ALLOWED_TYPES = {
            "<class 'ChatPermissions'>": self.convert_chat_permissions,
            "<class 'NoneType'>": self.none
        }

        if self.type not in ALLOWED_TYPES.keys(): raise TypeError
        return ALLOWED_TYPES[self.type]()

    @staticmethod
    def none() -> str:
        return "{}"

    def convert_chat_permissions(self) -> str:
        data = self.obj.__dict__
        del data["_client"]
        return json.dumps(data)


class GetOrCreate:
    def __init__(
            self,
            message: Message | None = None,
            user: User | None = None,
            chat: Chat | None = None
    ):
        if not message and (not user or not chat): raise LowArgs

        self.pg_chat = message.chat if chat is None else chat
        self.pg_user = message.from_user if user is None else user

    @property
    def chat(self) -> Chats:
        return Chats.get_or_create(id_in_telegram=self.pg_chat.id)[0]

    @property
    def user(self) -> Users:
        return Users.get_or_create(id_in_telegram=self.pg_user.id)[0]

    async def chat_member(self) -> ChatMembers:
        member, created = ChatMembers.get_or_create(chat=self.chat, member=self.user)
        if not created: return member

        pg_member = await self.pg_chat.get_member(self.pg_user.id)
        ChatMemberSettings.create(
            custom_name=self.pg_user.first_name,
            admin_rights_lvl=100 if self.pg_user.id in OP_USERS else 0,
            permissions_json=JsonConverter(pg_member.permissions).json,
            member=member,
        )

        return member


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


def extract_arguments(text: str) -> str or None:
    regexp = re.compile(r"/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
    result = regexp.match(text)
    return result.group(2) if text.startswith('/') and text is not None else None


def safe_to_datetime(value: str, f: str = "%d/%m/%Y %H:%M") -> datetime | None:
    try:
        return datetime.strptime(value, f)
    except ValueError:
        return None
