# -*- coding: utf-8 -*-
__all__ = ["start_router", "command_start_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from sqlalchemy import select

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.bot.menu.settings_menu import get_settings_menu_root
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.database.model import User, AppRole, Chat, ChatMember, ChatSetting
from quackamollie.core.enum.chat_type import ChatType
from quackamollie.core.enum.role_type import AppRoleType
from quackamollie.core.enum.user_type import UserType
from quackamollie.core.utils.str_management import sanitize_username

log = logging.getLogger(__name__)

start_router = Router()


@start_router.message(CommandStart())
@permission_authorized
@acknowledge_with_reactions
@pass_quackamollie_settings
async def command_start_handler(quackamollie_settings: QuackamollieSettings, message: Message):
    """ Handler for the `/start` command in Telegram chat

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param message: The message as given by aiogram router
        :type message: Message
    """
    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get user info from message
    user_id: int = message.from_user.id
    user_name: str = sanitize_username(message.from_user.full_name)
    user_role: AppRoleType = AppRoleType.authorized
    if user_id in quackamollie_settings.admin_ids:
        user_role = AppRoleType.admin
    elif user_id in quackamollie_settings.moderator_ids:
        user_role = AppRoleType.moderator

    # Get chat info from message
    chat_id: int = message.chat.id
    chat_name: str = f"Private chat of {user_name}" if message.chat.title is None else message.chat.title
    chat_type: ChatType = ChatType[message.chat.type]

    # Get user object, chat object and chat_member relationship references to know if they already exists or not
    async with async_session() as session:
        user_result = await session.execute(select(User.id).where(User.id == user_id).limit(1))
        user = user_result.scalars().first()
        chat_result = await session.execute(select(Chat.id).where(Chat.id == chat_id).limit(1))
        chat = chat_result.scalars().first()
        chat_member_stmt = select(ChatMember.chat_id).where((ChatMember.user_id == user_id) &
                                                            (ChatMember.chat_id == chat_id)).limit(1)
        chat_member_result = await session.execute(chat_member_stmt)
        chat_member = chat_member_result.scalars().first()

    objects_to_create = []
    relationships_to_create = []

    # Add user for creation if not found
    if user is None:
        log.debug("The user is not found in the database. Creating them...")

        async with async_session() as session:
            role_result = await session.execute(select(AppRole.id).where(AppRole.role_type == user_role).limit(1))
            role_id = role_result.scalars().one()

        new_user = User(
            id=user_id,
            user_type=UserType.user,
            app_role_id=role_id,
            full_name=user_name,
            username=sanitize_username(message.from_user.username),
            first_name=sanitize_username(message.from_user.first_name),
            last_name=sanitize_username(message.from_user.last_name),
        )
        objects_to_create.append(new_user)
    else:
        log.debug(f"User '{user_name}' with ID '{user_id}' already exists in the database")

    # Add chat for creation if not found
    if chat is None:
        log.debug("The chat is not found in the database. Creating it...")
        objects_to_create.append(Chat(id=chat_id, chat_name=chat_name, chat_type=chat_type,
                                      settings=ChatSetting()))
    else:
        log.debug(f"Chat '{chat_name}' with ID '{chat_id}' already exists in the database")

    # Add chat_member for creation if not found
    if chat_member is None:
        log.debug("The relationship between user and chat is not found in the database. Creating it...")
        relationships_to_create.append(ChatMember(user_id=user_id, chat_id=chat_id))
    else:
        log.debug(f"Relationship between user '{user_id}' and chat '{chat_id}' already exists in the database")

    # If the resources to create list is not empty, we create the needed resources
    if objects_to_create or relationships_to_create:
        async with async_session() as session:
            if objects_to_create:
                async with session.begin():
                    session.add_all(objects_to_create)
            if relationships_to_create:
                async with session.begin():
                    session.add_all(relationships_to_create)

        log.debug("Missing resources created with success")
        start_message = (f"Welcome, <b>{user_name}</b>!\nYou successfully registered in this chat. Now, you may want"
                         f" to edit chat settings to set the LLM model to use in this chat.")
    else:
        start_message = f"Welcome, <b>{user_name}</b>!\nYou are already registered in this chat."

    # Get InlineKeyboardBuilder depending on the current type of chat and user AppRoleType
    start_builder = get_settings_menu_root(chat_type, user_role)

    # Reply the constructed answer
    await message.answer(
        start_message,
        parse_mode=ParseMode.HTML,
        reply_markup=start_builder.as_markup(),
        disable_web_page_preview=True,
    )
