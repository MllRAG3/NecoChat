from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.database import GetOrCreate, models
from modules.util import extract_arguments
from modules.filters import chat_is_group_filter


class ChangeCustomNameProcess(BaseHandler):
    __name__ = "обработчик команды /change_my_name"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("change_my_name") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        member = await GetOrCreate(message=message).chat_member()
        old_name, new_name = member.config[0].custom_name, extract_arguments(message.text)
        member.config[0].custom_name = new_name
        models.ChatMemberSettings.save(member.config[0])

        await message.reply(f"{old_name} теперь {new_name}, выпьем же! )")
