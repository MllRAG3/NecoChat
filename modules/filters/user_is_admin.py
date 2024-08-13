from modules.filters.user_is_op import user_is_op
from pyrogram import types
from modules.database import GetOrCreate


async def user_is_admin(message: types.Message, req_lvl: int = 1, alert: bool = True) -> bool:
    member = await GetOrCreate(message=message).chat_member()
    if member.config[0].admin_rights_lvl >= req_lvl: return True
    if await user_is_op(message, alert=False): return True

    if alert: await message.reply(
        f"Твой уровень {member.config[0].admin_rights_lvl} слишком низок (требуется {req_lvl}), ты не можешь "
        f"использовать команду {message.command[0]}, иди гуляй!"
    )

    return False
