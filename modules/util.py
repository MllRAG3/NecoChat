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
