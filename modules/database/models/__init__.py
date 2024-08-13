from .chats import Chats, ChatMembers, ChatMemberSettings, Messages
from .users import Users
from .f_words import ForbiddenWords
from .next_step_records import NSRec

models: list = [
    Users,

    Chats,
    ChatMemberSettings,
    ChatMembers,
    Messages,

    ForbiddenWords,

    NSRec,
]
