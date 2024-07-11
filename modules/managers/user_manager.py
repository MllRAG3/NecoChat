from modules.managers.chat_manager import ChatManager
from modules.database.models import Users, ChatMembers
from modules.config import OP_USERS
from modules.bot import Il

from pyrogram.types import User, Chat, ChatMember
import json


class UserManager:
    def __init__(self, user: User, chat: Chat):
        self.user: User = user
        self.chat: Chat = chat

    @property
    def from_database(self) -> tuple[Users, ChatMembers]:
        """
        Возникают исключения:
          DoesNotExist если пользователя нет в базе данных
        :return: Запись из бд если та присутствует
        """
        user = Users.get(id_in_telegram=self.user.id)
        return user, ChatMembers.get(member=user)

    async def create_database_user(self) -> tuple[Users, ChatMembers]:
        data = {
            "id_in_telegram": self.user.id,
            "custom_name": self.user.first_name,
            "admin_rights_lvl": 100 if self.user.id in OP_USERS else 0  # пока что так
        }
        db_user = Users.create(**data)

        data = {
            "chat": ChatManager(self.chat).from_database,
            "member": db_user,
            "permissions_json": await self.current_permissions()
        }
        like_chat_member = ChatMembers.create(**data)

        return db_user, like_chat_member

    async def current_permissions(self) -> str:
        member: ChatMember = await Il.get_chat_member(self.chat.id, self.user.id)
        permissions = member.permissions
        return json.dumps({
            "can_send_messages": permissions.can_send_messages,
            "can_send_media_messages": permissions.can_send_media_messages,
            "can_send_other_messages": permissions.can_send_other_messages,
            "can_send_polls": permissions.can_send_polls,
            "can_add_web_page_previews": permissions.can_add_web_page_previews,
            "can_change_info": permissions.can_change_info,
            "can_invite_users": permissions.can_invite_users,
            "can_pin_messages": permissions.can_pin_messages,
        })

    @staticmethod
    def save(new):
        Users.save(new)
