from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import UserManager
from modules.filters import command_is_reply, user_is_op, user_is_admin, chat_is_group


class KillProcess(BaseHandler):
    __name__ = "Обработчик команды /kill"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("kill")

    async def func(self, _, message: types.Message):
        if not await command_is_reply(message): return
        if await user_is_op(message, user=message.reply_to_message.from_user): return
        if not await user_is_admin(message): return
        if not await chat_is_group(message): return

        await message.chat.ban_member(message.reply_to_message.from_user.id)
        await message.reply(
            f"{UserManager(message.from_user).from_database.custom_name} жестоко прикончил "
            f"{UserManager(message.reply_to_message.from_user).from_database.custom_name}"
            f"\n\nБольше в этом чате вы его не увидите.."
        )
