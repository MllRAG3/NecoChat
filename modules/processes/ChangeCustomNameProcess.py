from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.database.models import Users
from modules.util import get_user_from_db, extract_arguments


class ChangeCustomNameProcess(BaseHandler):
    __name__ = "обработчик команды /ChangeName"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("ChangeName")

    async def func(self, _, message: types.Message):
        db_user = await get_user_from_db(message=message)
        old_name, new_name = db_user[0].custom_name, extract_arguments(message.text)
        db_user[0].custom_name = new_name
        Users.save(db_user[0])

        await message.reply(f"{old_name} теперь {new_name}, выпьем же! )")
