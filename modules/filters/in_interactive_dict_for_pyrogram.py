from pyrogram import types, filters
from modules.config import analyzer


def iid(_, __, message: types.Message):
    if not message or not message.text or not message.reply_to_message: return False

    first_word = message.text.split()[0].strip().lower()
    anal_version = analyzer.parse(first_word)[0]

    if first_word != anal_version.normal_form: return False
    if not ({"INFN", "perf"} in anal_version.tag): return False

    return True


in_interactive_dict_filter = filters.create(iid)
