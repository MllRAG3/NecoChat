from pyrogram import types
from modules.util import UserManager


async def user_is_admin(message: types.Message, user: types.User | None = None, req_lvl: int = 1) -> bool:
    if user is None: user = message.from_user
    if UserManager(user, message.chat).from_database.admin_rights_lvl >= req_lvl: return True

    await message.reply(
        f"Ты не админ, иди гуляй "
        f"({UserManager(message.reply_to_message.from_user).from_database.custom_name} остается при своем положении)"
    )
    return False
