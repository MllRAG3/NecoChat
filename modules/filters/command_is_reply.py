from pyrogram import types


async def command_is_reply(message: types.Message, alert: bool = True) -> bool:
    if message.reply_to_message: return True
    if alert: await message.reply("Команда должна быть использована реплаем!")
    return False
