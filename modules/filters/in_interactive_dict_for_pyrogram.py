from pyrogram import types, filters
from modules.config import INTERACTIVE


def iid(_, __, message: types.Message):
    return message and message.text and (message.text.lower().strip() in INTERACTIVE.keys()) and message.reply_to_message


in_interactive_dict_filter = filters.create(iid)
