# -*- coding: utf-8 -*-
""" Module to access the `/settings` menu from the Telegram bot"""
__all__ = ["settings_router", "command_settings_handler", "root_settings_callback_handler", "answer_root_settings"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from typing import Optional, Union

from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.decorator.user_chat_registered import ensure_user_chat_registered
from quackamollie.core.bot.menu.settings_menu import (SettingsCallbackData, get_settings_menu_root,
                                                      get_settings_menu_root_description)
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.database.model import ChatSetting
from quackamollie.core.enum.chat_type import ChatType
from quackamollie.core.enum.role_type import AppRoleType

log = logging.getLogger(__name__)

settings_router = Router()


@settings_router.message(Command("settings"))
@permission_authorized
@ensure_user_chat_registered
@acknowledge_with_reactions
@pass_quackamollie_settings
async def command_settings_handler(quackamollie_settings: QuackamollieSettings, message: Message):
    """ Handler for the `/settings` command in Telegram chat.

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param message: The message as given by aiogram router
        :type message: Message
    """
    await answer_root_settings(quackamollie_settings, message)


@settings_router.callback_query(SettingsCallbackData.filter(F.name == "settings_root"))
@permission_authorized
@ensure_user_chat_registered
@pass_quackamollie_settings
async def root_settings_callback_handler(quackamollie_settings: QuackamollieSettings, query: CallbackQuery):
    """ Callback query handler for when hitting a `go back` button redirecting to te settings root

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param query: A callback query given by aiogram
        :type query: CallbackQuery
    """
    await answer_root_settings(quackamollie_settings, query)


async def answer_root_settings(quackamollie_settings: QuackamollieSettings, query_msg: Union[Message, CallbackQuery]):
    """ Handler when asked to display the `/settings` command in Telegram chat or when hitting a `go back` button
        redirecting to te settings root

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param query_msg: Undifferentiated Message or CallbackQuery as given by aiogram router
        :type query_msg: Union[Message, CallbackQuery]
    """
    message: Message = query_msg.message if isinstance(query_msg, CallbackQuery) else query_msg

    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get user AppRoleType from the message and quackamollie_settings
    user_role: AppRoleType = AppRoleType.authorized
    if query_msg.from_user.id in quackamollie_settings.admin_ids:
        user_role = AppRoleType.admin
    elif query_msg.from_user.id in quackamollie_settings.moderator_ids:
        user_role = AppRoleType.moderator

    # Get chat info from message
    chat_id: int = message.chat.id
    chat_type: ChatType = ChatType[message.chat.type]

    # Get possible chat type override from database, if not already in a private chat
    if chat_type != ChatType.private:
        async with async_session() as session:
            # Get chat settings for the current chat
            chat_setting_result = await session.execute(select(ChatSetting).where(
                ChatSetting.chat_id == chat_id
            ).limit(1))
            chat_setting: Optional[ChatSetting] = chat_setting_result.scalars().first()

            # Get possible chat type override
            chat_type_override: Optional[ChatType] = chat_setting.chat_type_override
            if chat_type_override is not None:
                chat_type = chat_type_override

    # Get InlineKeyboardBuilder depending on the current type of chat and user AppRoleType
    settings_builder = get_settings_menu_root(chat_type, user_role)

    # Get menu descriptions depending on the current type of chat and user AppRoleType
    settings_message = get_settings_menu_root_description(chat_type, user_role)

    # Reply the constructed answer depending on the type of the given `query_msg`
    if isinstance(query_msg, CallbackQuery):
        # If this answer results from a CallbackQuery, we edit the current message
        await message.edit_text(
            settings_message,
            parse_mode=ParseMode.HTML,
            reply_markup=settings_builder.as_markup(),
            disable_web_page_preview=True,
        )
    else:
        # If this answer results from a Message (i.e. from the /settings command), we answer a new message
        await message.answer(
            settings_message,
            parse_mode=ParseMode.HTML,
            reply_markup=settings_builder.as_markup(),
            disable_web_page_preview=True,
        )
