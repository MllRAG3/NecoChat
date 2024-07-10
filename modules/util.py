from modules.database.models import models, Users
from modules.database import db
from modules.config import OP_USERS

from peewee import DoesNotExist
from pyrogram.types import User


def create_tables() -> None:
    """Database models to tables"""
    if not any(models):
        print("No database models created.")
        return
    with db:
        db.create_tables(models)
    print(f"created models: {', '.join(map(lambda x: x.__name__, models))}")


class UserManager:
    def __init__(self, user: User):
        self.user: User = user

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
            return Users.create(**data)
