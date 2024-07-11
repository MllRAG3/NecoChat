from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, types

from modules.util import UserManager
from modules.filters import in_interactive_dict_filter
from modules.config import INTERACTIVE

import random


class InteractiveProcess(BaseHandler):
    __name__ = "Интерактивный regexp"
    HANDLER = handlers.MessageHandler
    FILTER = in_interactive_dict_filter

    async def func(self, _, message: types.Message):
        res = INTERACTIVE[message.text.lower().strip()]
        if type(res) is list: res = random.choice(res)
        await message.reply(res.format(
            UserManager(message.from_user, message.chat).from_database.custom_name,
            UserManager(message.reply_to_message.from_user, message.chat).from_database.custom_name
        ))
