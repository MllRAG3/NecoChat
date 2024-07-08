from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import get_or_create_user


class KillProcess(BaseHandler):
    __name__ = "Обработчик команды /kill"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("kill")

    async def func(self, _, message: types.Message):
        if not message.reply_to_message:
            await message.reply("Команда должна быть использована реплаем!")
            return
        if not get_or_create_user(message).has_admin_rights:
            await message.reply(
                f"Ты не админ, иди гуляй "
                f"({get_or_create_user(message.reply_to_message.from_user).custom_name} остается жив)"
            )
            return
        if not (message.chat.type.GROUP or message.chat.type.SUPERGROUP):
            await message.reply("Шалун, эта команда только для группы или супергруппы")

        await message.chat.ban_member(message.reply_to_message.from_user.id)
        await message.reply(
            f"{get_or_create_user(message).custom_name} жестоко прикончил "
            f"{get_or_create_user(message.reply_to_message.from_user)}"
            f"\n\nБольше в этом чате вы его не увидите.."
        )
