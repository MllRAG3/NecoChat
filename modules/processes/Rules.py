import os

from modules.database.models import ChatRules
from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import extract_arguments
from modules.filters import chat_is_group_filter, user_is_admin
from modules.database import GetOrCreate

from modules.bot import Il


class AddRule(BaseHandler):
    __name__ = "/add_rule"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("add_rule") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        if not await user_is_admin(message, req_lvl=1): return
        try:
            title, text = extract_arguments(message.text).split("|")
            title = title.strip().upper()
            text = text.strip()
        except (TypeError, ValueError):
            await message.reply(
                "Неправильный формат команды!"
                "\nПример: /add_rule [название правила] | [текст правила]"
            )
            return

        ChatRules.create(
            title=title,
            text=text,
            chat=GetOrCreate(message=message).chat,
        )
        member = await GetOrCreate(message=message).chat_member()
        await message.reply(
            f"{member.config[0].custom_name} добавил новое правило!"
        )


class RemoveRule(BaseHandler):
    __name__ = "/remove_rule"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("remove_rule") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        if not await user_is_admin(message, req_lvl=1): return

        title = extract_arguments(message.text).strip().upper()
        if title is None:
            await message.reply(
                "Неправильный формат команды!"
                "\nПример: /remove_rule [действующее название правила (выделяется **жирным**)]"
            )
            return
        if ChatRules.get_or_none(title=title, chat=GetOrCreate(message=message).chat) is None:
            await message.reply("Нет такого правила!")
            return

        ChatRules.delete_by_id(ChatRules.get(title=title, chat=GetOrCreate(message=message).chat))
        member = await GetOrCreate(message=message).chat_member()
        await message.reply(
            f"{member.config[0].custom_name} удалил правило (название: **{title}**)!"
        )


class RulesList(BaseHandler):
    __name__ = "/rules_list"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("rules_list") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        member = await GetOrCreate(message=message).chat_member()
        await message.reply(
            f"{member.config[0].custom_name} запросил список правил!"
            f"\nФайл будет отправлен лс...", quote=False
        )

        name = f"rules_chat_{message.chat.id}.txt"
        with open(name, "w") as f:
            rules = list(map(
                lambda x: "{}\n{}\n\n".format(x.title, x.text),
                GetOrCreate(message=message).chat.rules
            ))
            f.writelines(rules if rules else ["В ЧАТЕ НЕ ДОБАВЛЕНО ПРИАВИЛ! АНАРХИЯ:3"])
        try:
            await Il.send_document(
                chat_id=GetOrCreate(message=message).user.id_in_telegram,
                document=open(name, "rb"),
                caption=f"Список правил чата {message.chat.title}"
            )
        except Exception as e:
            await message.reply(f"Не могу отправить список правил лс!\nКод ошибки: {e}")

        os.remove(name)
