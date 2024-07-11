from modules.database.models.BaseModel import BaseModel
from peewee import IntegerField, BooleanField, CharField


class Users(BaseModel):
    id_in_telegram = IntegerField()
    custom_name = CharField()

    admin_rights_lvl = IntegerField()

    can_send_messages = BooleanField(default=True)
    can_send_media_messages = BooleanField(default=True)
    can_send_other_messages = BooleanField(default=True)
    can_send_polls = BooleanField(default=True)
    can_add_web_page_previews = BooleanField(default=True)
    can_change_info = BooleanField(default=False)
    can_invite_users = BooleanField(default=False)
    can_pin_messages = BooleanField(default=False)


FORM = {
    "can_send_messages": True,
    "can_send_media_messages": True,
    "can_send_other_messages": True,
    "can_send_polls": True,
    "can_add_web_page_previews": True,
    "can_change_info": True,
    "can_invite_users": True,
    "can_pin_messages": True,
}
