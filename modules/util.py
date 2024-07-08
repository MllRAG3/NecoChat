from modules.database.models import models, Users
from modules.database import db

from peewee import DoesNotExist, OperationalError
from pyrogram.types import Message, User


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


def get_or_create_user(message: Message | Users | None) -> Users | None:
    if message is None: return
    user: User = message if isinstance(message, User) else message.from_user
    try:
        return Users.get(id_in_telegram=user.id)
    except (DoesNotExist, OperationalError,):
        data = {
            "id_in_telegram": user.id,
            "custom_name": user.first_name,
            "has_admin_rights": user.id in [1044385209]
        }
        return Users.create(**data)
