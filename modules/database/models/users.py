from modules.database.models.BaseModel import BaseModel
from peewee import IntegerField


class Users(BaseModel):
    id_in_telegram = IntegerField()
