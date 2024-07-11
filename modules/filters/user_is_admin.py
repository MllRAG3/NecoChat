from pyrogram import types
from modules.util import get_user_from_db


async def user_is_admin(message: types.Message, user: types.User | None = None, req_lvl: int = 1) -> bool:
    if user is None: user = message.from_user
    db_user = await get_user_from_db(user=user, chat=message.chat)
    if db_user[0].admin_rights_lvl >= req_lvl: return True

    db_user = await get_user_from_db(user=message.reply_to_message.from_user, chat=message.chat)
    await message.reply(
        f"Ты не админ, иди гуляй!"
        f"\n{db_user[0].custom_name} остается при своем положении"
    )
    return False
