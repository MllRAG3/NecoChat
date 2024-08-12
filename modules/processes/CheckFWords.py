from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types, errors

from modules.config import analyzer
from modules.database import GetOrCreate
from modules.database.models import ForbiddenWords
from modules.filters import chat_is_group_filter

from datetime import datetime, timedelta


def get_f_words(message) -> list[str]:
    f_words = set(map(
        lambda x: x.word,
        ForbiddenWords.select().where(ForbiddenWords.chat == GetOrCreate(message=message).chat)
    ))
    m_words = set(map(
        lambda x: analyzer.parse(x)[0].normal_form,
        message.text.split()
    ))

    return list(m_words & f_words)


def in_f_list(_, __, message) -> bool:
    if get_f_words(message): return True
    return False


filter_for_check = filters.create(in_f_list)


class CheckFWords(BaseHandler):
    __name__ = "Проверка наличия запрещенных слов"
    HANDLER = handlers.MessageHandler
    FILTER = filter_for_check & chat_is_group_filter

    async def func(self, _, message: types.Message):
        await GetOrCreate(message=message).log()
        member = await GetOrCreate(message=message).chat_member()
        until_date = datetime.now() + timedelta(seconds=sum(map(
            lambda x: ForbiddenWords.get(word=x).restrict_time,
            get_f_words(message)
        )))
        try:
            await message.delete()
            await message.chat.restrict_member(
                message.from_user.id,
                types.ChatPermissions(),
                until_date=until_date
            )
            await message.reply(
                f"Пользователь {member.config[0].custom_name} лишен права голоса до {until_date} за использование "
                f"запрещенных слов!"
                f"\nСписок можно посмотреть по команде /list_of_f_words")
        except errors.UserAdminInvalid:
            pass
