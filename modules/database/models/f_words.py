from modules.database.models.BaseModel import BaseModel
from modules.database.models.chats import Chats
from peewee import CharField, ForeignKeyField


class ForbiddenWords(BaseModel):
    word = CharField()
    chat = ForeignKeyField(Chats, backref="forbidden_words")
