from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import extract_arguments, safe_to_datetime
from modules.filters import command_is_reply, user_is_op, user_is_admin, chat_is_group
from modules.database import GetOrCreate

import json


class KillProcess(BaseHandler):
    __name__ = "Обработчик команды /kill"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("kill")

    async def func(self, _, message: types.Message):
        if not await command_is_reply(message): return
        if await user_is_op(message, user=message.reply_to_message.from_user): return
        if not await user_is_admin(message): return
        if not await chat_is_group(message): return

        reply_member = await GetOrCreate(message=message, user=message.reply_to_message.from_user).chat_member()
        cmd_member = await GetOrCreate(message=message).chat_member()

        await message.chat.ban_member(message.reply_to_message.from_user.id)
        await message.reply(
            f"{cmd_member.config.custom_name} жестоко прикончил {reply_member.config.custom_name}"
            f"\n\nБольше в этом чате вы его не увидите.."
        )


class ShutUpProcess(BaseHandler):
    __name__ = "Обработчик команды /shutup"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command('shutup')

    async def func(self, _, message: types.Message):
        if not await command_is_reply(message): return
        if await user_is_op(message, user=message.reply_to_message.from_user): return
        if not await user_is_admin(message): return
        if not await chat_is_group(message): return

        until_date = safe_to_datetime(extract_arguments(message.text))
        if until_date is None:
            await message.reply(
                "Указан неправильный формат времени мьюта!"
                "\n\nПравильный формат:"
                "\n<b>день/месяц/год чч:мм</b>"
                "\n(например 6/8/2003 10:56)"
                "\n\nЕсли время меньше 30 сек или больше года, то срок будет выставлен на бесконечный"
            )
            return

        reply_member = await GetOrCreate(message=message, user=message.reply_to_message.from_user).chat_member()

        await message.chat.restrict_member(
            message.reply_to_message.from_user.id,
            types.ChatPermissions(),
            until_date=until_date
        )
        await message.reply(f"Пользователь {reply_member.config.custom_name} лишен права голоса до {until_date}!")


class UnmuteProcess(BaseHandler):
    __name__ = "Обработчик команды /unmute"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command('unmute')

    async def func(self, _, message: types.Message):
        if not await command_is_reply(message): return
        if not await user_is_admin(message): return
        if not await chat_is_group(message): return

        reply_member = await GetOrCreate(message=message, user=message.reply_to_message.from_user).chat_member()

        await message.chat.restrict_member(
            message.reply_to_message.from_user.id,
            types.ChatPermissions(**json.loads(reply_member.config.permissions_json))
        )

        await message.reply(f"Пользователь {reply_member.config.custom_name} освобожден досрочно!")
