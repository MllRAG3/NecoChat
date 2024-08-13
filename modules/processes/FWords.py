import os

from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types

from modules.util import extract_arguments
from modules.config import analyzer
from modules.database import GetOrCreate, db
from modules.database.models import ForbiddenWords
from modules.filters import chat_is_group_filter


class AddFWord(BaseHandler):
    __name__ = "/add_f_word"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("add_f_word") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        try:
            word, rtime = extract_arguments(message.text).split()
            rtime = int(rtime)
        except (TypeError, ValueError) as e:
            await message.reply(
                "Неправильный формат команды!"
                "\nПример: /add_f_word [слово] [время мьюта за употребление, число, сек]"
            )
            return
        word = analyzer.parse(word)[0].normal_form
        ForbiddenWords.get_or_create(
            word=word,
            restrict_time=rtime,
            chat=GetOrCreate(message=message).chat
        )

        await message.reply(f"Слово {word.capitalize()} пополнило список запрещенных! (наказание -- мьют на {rtime} сек.)")


class RemoveFWord(BaseHandler):
    __name__ = "/remove_f_word"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("remove_f_word") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        data = GetOrCreate(message=message)
        await data.log()
        word = extract_arguments(message.text)
        if not word:
            await message.reply("Слово для удаления из списка должно быть указано после команды!")
            return
        word = analyzer.parse(word)[0].normal_form
        db.execute(ForbiddenWords.delete().where(
            (ForbiddenWords.chat == data.chat) &
            (ForbiddenWords.word == word)
        ))

        await message.reply(f"Слово {word.capitalize()} исключено из списка запрещенных, выпьем же!")


class FWordsList(BaseHandler):
    __name__ = "/list_of_f_words"
    HANDLER = handlers.MessageHandler
    FILTER = filters.command("list_of_f_words") & chat_is_group_filter

    async def func(self, _, message: types.Message):
        data = GetOrCreate(message=message)
        await data.log()
        way = f"fws_chat_{message.chat.id}.docx"
        with open(way, "w") as f:
            f.write('\n'.join(map(
                lambda x: x.word + f" (Наказание - мьют на {x.restrict_time} сек)",
                ForbiddenWords.select().where(ForbiddenWords.chat == data.chat)
            )))

        await message.reply_document(document=open(way, "rb"), caption="Список запрещенных слов!")
        os.remove(way)
