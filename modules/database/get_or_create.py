from modules.config import OP_USERS
from .models import ChatMembers, ChatMemberSettings, Chats, Users, Messages
from modules.errors import LowArgs
from modules.util import JsonConverter

from pyrogram.types import Message, Chat, User


class GetOrCreate:
    def __init__(
            self,
            *,
            message: Message | None = None,
            user: User | None = None,
            chat: Chat | None = None
    ):
        if not message and (not user or not chat): raise LowArgs

        self.pg_chat = message.chat if chat is None else chat
        self.pg_user = message.from_user if user is None else user

    @property
    def chat(self) -> Chats:
        return Chats.get_or_create(id_in_telegram=self.pg_chat.id)[0]

    @property
    def user(self) -> Users:
        return Users.get_or_create(id_in_telegram=self.pg_user.id)[0]

    async def chat_member(self) -> ChatMembers:
        member, created = ChatMembers.get_or_create(chat=self.chat, member=self.user)
        if not created: return member

        pg_member = await self.pg_chat.get_member(self.pg_user.id)
        ChatMemberSettings.create(
            custom_name=self.pg_user.first_name,
            admin_rights_lvl=100 if self.pg_user.id in OP_USERS else 0,
            permissions_json=JsonConverter(pg_member.permissions).json,
            member=member,
        )

        return member

    async def log(self):
        Messages.create(
            sender=await self.chat_member()
        )
