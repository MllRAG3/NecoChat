from modules.processes.BaseHandler import BaseHandler
from pyrogram import handlers, filters, types, errors

from modules.config import analyzer, MUTE_TIME_FOR_F_WORD
from modules.database import GetOrCreate
from modules.database.models import ForbiddenWords

from datetime import datetime, timedelta


def in_f_list(_, __, message):
    f_words = set(map(
        lambda x: x.word,
        ForbiddenWords.select().where(ForbiddenWords.chat == GetOrCreate(message=message).chat)
    ))
    m_words = set(map(
        lambda x: analyzer.parse(x)[0].normal_form,
        message.text.split()
    ))

    if m_words & f_words: return True
    return False


filter_for_check = filters.create(in_f_list)


class CheckFWords(BaseHandler):
    __name__ = "Проверка наличия запрещенных слов"
    HANDLER = handlers.MessageHandler
    FILTER = filter_for_check

    async def func(self, _, message: types.Message):
        member = await GetOrCreate(message=message).chat_member()
        until_date = datetime.now() + timedelta(seconds=MUTE_TIME_FOR_F_WORD)
        try:
            await message.delete()
            await message.chat.restrict_member(
                message.from_user.id,
                types.ChatPermissions(),
                until_date=until_date
            )
            await message.reply(
                f"Пользователь {member.config[0].custom_name} лишен права голоса до {until_date} за использование "
                f"запрещенных слов! Спосок можно посмотреть по команде /list_of_f_words")
        except errors.UserAdminInvalid:
            pass
