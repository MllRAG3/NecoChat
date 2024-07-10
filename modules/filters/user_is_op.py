from pyrogram import types
from modules.config import OP_USERS
from modules.util import UserManager


async def user_is_op(message: types.Message, user: types.User | None = None) -> bool:
    if user is None: user = message.from_user
    if user.id not in OP_USERS: return False
    await message.reply(
        f"{UserManager(message.reply_to_message.from_user).from_database.custom_name} "
        f"слишком ценный член для этого чата, его нельзя бить и команда /{message.command[0]} не может быть "
        f"использована на нем )"
    )
    return True
