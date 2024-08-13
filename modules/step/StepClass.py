from pyrogram import types
import ctypes
from typing import Callable, Any

from modules.database import GetOrCreate
from modules.database.models import NSRec, ChatMembers


class Step:
    __name__ = "StepFilter"

    def __init__(self, **client_data) -> None:
        """
        :param client_data: Информация о клиенте. Объект класса pyrogram.types.Message или
        pyrogram.types.Chat и pyrogram.types.User
        """
        self.client_data = client_data

    async def register(self, func: Callable) -> None:
        """Зарегистрировать ожидание след. сообщения"""
        client = await GetOrCreate(**self.client_data).chat_member()
        NSRec.create(client=client, func_id=id(func))

    async def clear(self) -> None:
        """Очистить ожидание след. сообщения"""
        client = await GetOrCreate(**self.client_data).chat_member()
        if not self.exist(client): return

        NSRec.delete_by_id(NSRec.get(client=client))

    async def get_and_execute(self, message: types.Message) -> Any:
        """Получить и исполнить зарегистрированную запись"""
        client = await GetOrCreate(**self.client_data).chat_member()
        if not self.exist(client): return

        call_res = await ctypes.cast(NSRec.get(client=client).func_id, ctypes.py_object).value(message=message)
        NSRec.delete_by_id(NSRec.get(client=client))
        return call_res

    @staticmethod
    def exist(client: ChatMembers) -> bool:
        """Есть ли зарегистрированные записи"""
        return NSRec.get_or_none(client=client) is not None

    async def __call__(self, _, msg: types.Message):
        client = await GetOrCreate(message=msg).chat_member()
        return self.exist(client)
