from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, types

from modules.database import GetOrCreate
from modules.filters import in_interactive_filter, chat_is_group_filter
from modules.config import analyzer


class InteractiveProcess(BaseHandler):
    __name__ = "Интерактивный regexp"
    HANDLER = handlers.MessageHandler
    FILTER = in_interactive_filter & chat_is_group_filter

    async def func(self, _, message: types.Message):
        text = message.text.split()
        first_word = text[0]
        anal_version = analyzer.parse(first_word)[0]

        text[0] = anal_version.inflect({"masc", "perf"})[0]  # + "(а)"
        text = ["{}"] + [text[0]] + ["{}"] + text[1:]

        reply_member = await GetOrCreate(message=message, user=message.reply_to_message.from_user).chat_member()
        cmd_member = await GetOrCreate(message=message).chat_member()

        result = " ".join(text).format(
            cmd_member.config[0].custom_name,
            reply_member.config[0].custom_name
        )

        await message.reply(result)
