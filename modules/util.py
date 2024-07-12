from modules.database.models import models
from modules.database import db

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
