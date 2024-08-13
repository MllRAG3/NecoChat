from pyrogram import types
import ctypes
from typing import Callable

from modules.database import GetOrCreate
from modules.database.models import NSRec, ChatMembers


class Step:
    __name__ = "StepFilter"

    def __init__(self, **client_data):
        self.client_data = client_data

    async def register(self, func: Callable):
        client = await GetOrCreate(**self.client_data).chat_member()
        NSRec.create(client=client, func_id=id(func))

    async def clear(self):
        client = await GetOrCreate(**self.client_data).chat_member()
        NSRec.delete().where(NSRec.client == client)

    async def get_and_execute(self, message: types.Message):
        client = await GetOrCreate(**self.client_data).chat_member()
        if not self.exist(client): return

        return await ctypes.cast(NSRec.get_or_none(client=client).func_id, ctypes.py_object).value(message=message)

    @staticmethod
    def exist(client: ChatMembers) -> bool:
        return NSRec.get_or_none(client=client) is not None

    async def __call__(self, _, msg: types.Message):
        client = await GetOrCreate(message=msg).chat_member()
        return self.exist(client)
