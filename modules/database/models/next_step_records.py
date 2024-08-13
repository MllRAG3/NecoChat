from modules.database.models.BaseModel import BaseModel
from modules.database.models.chats import ChatMembers
from peewee import ForeignKeyField, IntegerField


class NSRec(BaseModel):
    client = ForeignKeyField(ChatMembers, backref="next_steps")
    func_id = IntegerField()
