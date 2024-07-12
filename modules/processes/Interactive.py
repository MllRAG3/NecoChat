from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, types

from modules.util import get_user_from_db
from modules.filters import in_interactive_filter
from modules.config import analyzer


class InteractiveProcess(BaseHandler):
    __name__ = "Интерактивный regexp"
    HANDLER = handlers.MessageHandler
    FILTER = in_interactive_filter

    async def func(self, _, message: types.Message):
        text = message.text.split()
        first_word = text[0]
        anal_version = analyzer.parse(first_word)[0]

        text[0] = anal_version.inflect({"masc", "perf"})[0]  # + "(а)"
        text = ["{}"] + [text[0]] + ["{}"] + text[1:]

        reply_user = await get_user_from_db(message=message, user=message.reply_to_message.from_user)
        non_reply_user = await get_user_from_db(message=message)

        result = " ".join(text).format(
            non_reply_user[0].custom_name,
            reply_user[0].custom_name
        )

        await message.reply(result)
