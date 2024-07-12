from pyrogram import types, filters


async def chat_is_group(_, __, message: types.Message) -> bool:
    type = message.chat.type
    allowed = [type.GROUP, type.SUPERGROUP]

    if type not in allowed:
        await message.reply("Я работаю только в группах/супергруппах")
        return False

    return True


chat_is_group_filter = filters.create(chat_is_group)
