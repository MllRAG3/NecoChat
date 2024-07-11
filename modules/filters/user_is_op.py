from pyrogram import types
from modules.config import OP_USERS
from modules.util import get_user_from_db


async def user_is_op(message: types.Message, user: types.User | None = None) -> bool:
    if user is None: user = message.from_user
    if user.id not in OP_USERS: return False

    db_user = await get_user_from_db(message=message, user=message.reply_to_message.from_user)
    await message.reply(
        f"{db_user.custom_name} слишком ценный член этого чата, его нельзя бить и команда /{message.command[0]} "
        f"не может быть использована на нем )"
    )
    return True
