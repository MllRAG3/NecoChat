from .chats import Chats, ChatUsers
from .restrict_process import MutedUsers, KickedUsers
from .users import Users

models: list = [
    Users,

    Chats,
    ChatUsers,

    MutedUsers,
    KickedUsers,
]
