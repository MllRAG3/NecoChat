from modules.database.models.BaseModel import BaseModel
from modules.database.models.chats import ChatUsers
from peewee import DateTimeField, ForeignKeyField


class MutedUsers(BaseModel):
    user = ForeignKeyField(ChatUsers, backref="is_muted")
    until_date = DateTimeField()


class KickedUsers(BaseModel):
    user = ForeignKeyField(ChatUsers, backref="is_kicked")
    until_date = DateTimeField()
