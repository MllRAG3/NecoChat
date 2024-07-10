from modules.database.models.BaseModel import BaseModel
from peewee import IntegerField, BooleanField, CharField


class Users(BaseModel):
    id_in_telegram = IntegerField()
    custom_name = CharField()

    admin_rights_lvl = IntegerField()
