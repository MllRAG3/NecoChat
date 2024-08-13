from pyrogram import types
from modules.config import OP_USERS
from modules.database import GetOrCreate


async def user_is_op(message: types.Message, user: types.User | None = None, alert: bool = True) -> bool:
    if user is None: user = message.from_user
    if user.id not in OP_USERS: return False

    member = await GetOrCreate(message=message, user=user).chat_member()
    if alert: await message.reply(
        f"{member.config[0].custom_name} слишком ценный член этого чата, его нельзя бить и команда /{message.command[0]} "
        f"не может быть использована на нем )"
    )
    return True
