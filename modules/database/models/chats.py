from modules.database.models.BaseModel import BaseModel
from modules.database.models.users import Users
from peewee import IntegerField, ForeignKeyField, CharField


class Chats(BaseModel):
    id_in_telegram = IntegerField()
    custom_title = CharField()


class ChatUsers(BaseModel):
    chat = ForeignKeyField(Chats, backref="members")
    member = ForeignKeyField(Users, backref="chats")
