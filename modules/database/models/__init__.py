from .chats import Chats, ChatMembers, ChatMemberSettings, Messages, ChatRules
from .users import Users
from .f_words import ForbiddenWords
from .next_step_records import NSRec

models: list = [
    Users,

    Chats,
    ChatRules,
    ChatMemberSettings,
    ChatMembers,
    Messages,

    ForbiddenWords,

    NSRec,
]
