import os

from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types
from modules.database import GetOrCreate
from modules.filters import chat_is_group_filter
from modules.database.models import Messages

from modules.util import make_plt_pic, get_all_logs_grouped_by_days, get_all_today_hours
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
        member = await GetOrCreate(message=message).chat_member()
        now: datetime = datetime.now()
        per_day = len(Messages.select().where(
            Messages.updated_at.between(now - timedelta(days=1), now) & Messages.sender == member))
        per_week = len(Messages.select().where(
            Messages.updated_at.between(now - timedelta(days=7), now) & Messages.sender == member))
        per_month = len(Messages.select().where(
            Messages.updated_at.between(now - timedelta(days=30), now) & Messages.sender == member))
        per_all = len(Messages.select())

        await message.reply_photo(
            photo=open(make_plt_pic(
                cust_num=-1,
                today=get_all_today_hours(member),
                all_time=get_all_logs_grouped_by_days(member),
            ), "rb"),
            caption=f"Сообщения пользователя {member.config[0].custom_name}"
                    f"\nДень | Неделя | Месяц | Все время"
                    f"\n{per_day} | {per_week} | {per_month} | {per_all}"
        )
        os.remove("-1.png")


class SendChatStats(BaseHandler):  # beta
    __name__ = "Обработчик команды /chat"
    HANDLER = handlers.MessageHandler
    FILTER = None

    async def func(self, _, message: types.Message):
        pass
