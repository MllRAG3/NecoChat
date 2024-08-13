import re
from datetime import datetime

from modules.database.models import models
from modules.database import db


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
