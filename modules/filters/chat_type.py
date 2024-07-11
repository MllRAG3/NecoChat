from pyrogram import types


async def chat_is_group(message: types.Message, chat: types.Chat | None = None) -> bool:
    if chat is None: chat = message.chat
    if chat.type.GROUP or chat.type.SUPERGROUP: return True

    await message.reply("Шалун, эта команда только для группы или супергруппы")
    return False


async def chat_is_private(message: types.Message, chat: types.Chat | None = None) -> bool:
    if chat is None: chat = message.chat
    if chat.type.PRIVATE: return True

    await message.reply("Шалун, эта команда только для приватных чатов")
    return False
