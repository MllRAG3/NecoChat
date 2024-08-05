from pyrogram import types
from modules.database import GetOrCreate


async def user_is_admin(message: types.Message, req_lvl: int = 1) -> bool:
    member = await GetOrCreate(message=message).chat_member()
    if member.config[0].admin_rights_lvl >= req_lvl: return True

    reply_member = await GetOrCreate(message=message, user=message.reply_to_message.from_user).chat_member()
    await message.reply(
        f"Твой уровень {member.config[0].admin_rights_lvl} слишком низок (требуется {req_lvl}), ты не можешь использовать "
        f"команду {message.command[0]}, иди гуляй!"
        f"\n{reply_member.config[0].custom_name} остается при своем положении"
    )

    return False
