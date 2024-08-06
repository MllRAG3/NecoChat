from .chats import Chats, ChatMembers, ChatMemberSettings
from .users import Users
from .f_words import ForbiddenWords

models: list = [
    Users,

    Chats,
    ChatMemberSettings,
    ChatMembers,

    ForbiddenWords,
]
