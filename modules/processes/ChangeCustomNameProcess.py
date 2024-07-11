from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import UserManager, extract_arguments


class ChangeCustomNameProcess(BaseHandler):
    __name__ = "обработчик команды /ChangeName"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("ChangeName")

    async def func(self, _, message: types.Message):
        db_user = UserManager(message.from_user, message.chat).from_database
        old_name, new_name = db_user.custom_name, extract_arguments(message.text)
        db_user.custom_name = new_name
        UserManager.save(db_user)

        await message.reply(f"{old_name} теперь {new_name}, выпьем же! )")
