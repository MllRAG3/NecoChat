from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types
from modules.database import GetOrCreate
from modules.filters import chat_is_group_filter

from modules.step_stuff import Step


async def greet(message):
    await message.reply(message.text)


class StartProcess(BaseHandler):
    __name__ = "Обработчик команды /start"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("start") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        member = await GetOrCreate(message=message).chat_member()
        await message.reply(f"Привет, <b>{member.config[0].custom_name}</b>!")
        await Step(message=message).register(func=greet)
