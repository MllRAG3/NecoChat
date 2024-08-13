from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types
from modules.database import GetOrCreate
from modules.filters import chat_is_group_filter
from modules.util import StatsManager


class FinalLog(BaseHandler):
    __name__ = "Финальный статистический счетчик"
    HANDLER = handlers.MessageHandler
    FILTER = chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()


class SendUserStats(BaseHandler):
    __name__ = "Обработчик команды /me"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("me") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        member = await GetOrCreate(message=message).chat_member()

        await message.reply("Подожди, статистика загружается.. (займет 10~45сек)", quote=False)
        await message.reply_photo(**StatsManager(member=member).de_send)


class SendChatStats(BaseHandler):  # beta
    __name__ = "Обработчик команды /chat"
    HANDLER = handlers.MessageHandler
    FILTER = None

    async def func(self, _, message: types.Message):
        pass
