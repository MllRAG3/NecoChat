from modules.database.models import models, Users, ChatMembers
from modules.database import db
from modules.errors import LowArgs
from modules.managers import UserManager

from peewee import DoesNotExist
from datetime import datetime
from pyrogram.types import User, Chat, Message
import re


async def get_user_from_db(
        *,
        message: Message | None = None,
        user: User | None = None, chat: Chat | None = None
) -> tuple[Users, ChatMembers]:
    if not message and (not chat or not user): raise LowArgs("Необходимо указать или message или user и chat")
    if chat is None: chat = message.chat
    if user is None: user = message.from_user

    user_manag = UserManager(user, chat)
    try:
        return user_manag.from_database
    except DoesNotExist:
        db_create_r = await user_manag.create_database_user()
        return db_create_r


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


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


def safe_to_datetime(value: str, f: str = "%d/%m/%Y %H:%M") -> datetime | None:
    try:
        return datetime.strptime(value, f)
    except ValueError:
        return None
