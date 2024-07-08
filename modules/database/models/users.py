from modules.database.models.BaseModel import BaseModel
from peewee import IntegerField, BooleanField, CharField


class Users(BaseModel):
    id_in_telegram = IntegerField()
    custom_name = CharField()

    has_admin_rights = BooleanField()
    admin_rights_lvl = IntegerField(default=1)
