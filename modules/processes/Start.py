from . import BaseHandler as B
from pyrogram import handlers, filters, types

from modules.util import get_user_from_db


class StartProcess(B.BaseHandler):
    __name__ = "Обработчик команды /start"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("start")

    async def func(self, _, message: types.Message):
        db_user = await get_user_from_db(message=message)
        await message.reply(f"Привет, <b>{db_user[0].custom_name}</b>!")
