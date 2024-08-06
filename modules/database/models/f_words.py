from modules.database.models.BaseModel import BaseModel
from modules.database.models.chats import Chats
from peewee import CharField, ForeignKeyField, IntegerField


class ForbiddenWords(BaseModel):
    word = CharField()
    restrict_time = IntegerField(default=300)

    chat = ForeignKeyField(Chats, backref="forbidden_words")
