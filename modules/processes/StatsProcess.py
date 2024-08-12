from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types
from modules.database import GetOrCreate
from modules.filters import chat_is_group_filter
from modules.database.models import Messages

from datetime import datetime, timedelta


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
        now: datetime = datetime.now()
        per_day = len(Messages.select().where(Messages.updated_at.between(now - timedelta(seconds=10), now)))
        per_week = len(Messages.select().where(Messages.updated_at.between(now - timedelta(seconds=30), now)))
        per_month = len(Messages.select().where(Messages.updated_at.between(now - timedelta(seconds=60), now)))
        per_all = len(Messages.select())

        member = await GetOrCreate(message=message).chat_member()
        await message.reply(
            f"Сообщения пользователя {member.config[0].custom_name}"
            f"\nДень | Неделя | Месяц | Все время"
            f"\n{per_day} | {per_week} | {per_month} | {per_all}"
        )


class SendChatStats(BaseHandler):  # beta
    __name__ = "Обработчик команды /chat"
    HANDLER = handlers.MessageHandler
    FILTER = None

    async def func(self, _, message: types.Message):
        pass
