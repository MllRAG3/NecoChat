from modules.database.models.BaseModel import BaseModel
from modules.database.models.users import Users
from peewee import IntegerField, ForeignKeyField, CharField


class Chats(BaseModel):
    id_in_telegram = IntegerField()


class ChatRules(BaseModel):
    title = CharField()
    text = CharField()

    chat = ForeignKeyField(Chats, backref="rules")


class ChatMembers(BaseModel):
    chat = ForeignKeyField(Chats, backref="members")
    member = ForeignKeyField(Users, backref="chats")


class ChatMemberSettings(BaseModel):
    custom_name = CharField()
    admin_rights_lvl = IntegerField()
    permissions_json = CharField()

    member = ForeignKeyField(ChatMembers, backref="config")


class Messages(BaseModel):
    sender = ForeignKeyField(ChatMembers, backref="messages")
