from modules.database.models.BaseModel import BaseModel
from modules.database.models.users import Users
from peewee import IntegerField, ForeignKeyField, CharField, BooleanField


class Chats(BaseModel):
    id_in_telegram = IntegerField()
    custom_title = CharField()


class ChatMembers(BaseModel):
    chat = ForeignKeyField(Chats, backref="members")
    member = ForeignKeyField(Users, backref="chats")

    can_send_messages = BooleanField()
    can_send_media_messages = BooleanField()
    can_send_other_messages = BooleanField()
    can_send_polls = BooleanField()
    can_add_web_page_previews = BooleanField()
    can_change_info = BooleanField()
    can_invite_users = BooleanField()
    can_pin_messages = BooleanField()
