from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types
from modules.database import GetOrCreate


class StartProcess(BaseHandler):
    __name__ = "Обработчик команды /start"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("start")

    async def func(self, _, message: types.Message):
        member = await GetOrCreate(message=message).chat_member()
        await message.reply(f"Привет, <b>{member.config.custom_name}</b>!")
