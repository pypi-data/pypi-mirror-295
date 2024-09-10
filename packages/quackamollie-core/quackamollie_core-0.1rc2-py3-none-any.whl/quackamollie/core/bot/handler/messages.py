# -*- coding: utf-8 -*-
""" Module to define commands, handle additional configuration and start the bot """
__all__ = ["message_router", "handle_message"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from quackamollie.core.bot.bot_info import QuackamollieBotData
from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.bot.decorator.user_chat_registered import ensure_user_chat_registered
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.database.model import ChatSetting
from quackamollie.core.enum.chat_type import ChatType
from quackamollie.core.model_manager_registry.model_manager_registry import QuackamollieModelManagerRegistry

log = logging.getLogger(__name__)

message_router = Router()


def is_mentioned_in_group_or_supergroup(message: Message, mention: str, chat_type: ChatType):
    return (chat_type in [ChatType.group, ChatType.supergroup]
            and message.text and message.text.startswith(mention))


# TODO: Improving settings will lead to using finite state machines, ensure no state is defined when calling this
#       It should look like: @message_router.message(F.text, F.state == None)
#                            @message_router.message(F.caption, F.state == None)
@message_router.message(F.text)
@message_router.message(F.caption)
@permission_authorized
@ensure_user_chat_registered
@acknowledge_with_reactions
@pass_quackamollie_settings
async def handle_message(quackamollie_settings: QuackamollieSettings, message: Message):
    """ React on message with emojis. Answer user's message by using the model manager and model manager defined for
        the current chat of the defaults from settings. Handle only messages with text or captions and no finite state
        defined. Answer all messages in private chats (including chat types overridden from `/settings`). However,
        it only answers messages where the bot is explicitly mentioned at the beginning of the message
        in groups or supergroups.

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param message: The message as given by aiogram router
        :type message: Message
    """
    # Get mention and bot ID from pre-initialized bot data
    mention = QuackamollieBotData().bot_mention

    # Get model managers
    model_managers_by_entrypoint_name = QuackamollieModelManagerRegistry().model_managers
    model_managers_by_class_name = QuackamollieModelManagerRegistry().model_managers_by_class_name
    class_name_to_entrypoint_name = QuackamollieModelManagerRegistry().class_name_to_entrypoint_name

    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get chat info from message
    chat_id: int = message.chat.id
    chat_type: ChatType = ChatType[message.chat.type]

    # Get the current configuration for the chat from the database or from defaults
    async with async_session() as session:
        # Get chat settings for the current chat
        chat_setting_result = await session.execute(select(ChatSetting).where(
            ChatSetting.chat_id == chat_id
        ).limit(1).options(selectinload(ChatSetting.model_config)))
        chat_setting: Optional[ChatSetting] = chat_setting_result.scalars().first()

        # Get model settings for the current chat
        if chat_setting.model_config is not None:
            model_name = chat_setting.model_config.model_name
            model_config = chat_setting.model_config.config
            model_manager = await chat_setting.model_config.awaitable_attrs.model_manager_type
            if model_manager is not None:
                model_manager_class = model_managers_by_class_name.get(model_manager.model_manager_class, None)
            else:
                model_manager_class = None
            if model_manager_class is not None:
                model_manager_name = class_name_to_entrypoint_name.get(model_manager_class.__name__, None)
            else:
                model_manager_name = None
        else:
            model_name = quackamollie_settings.default_model
            model_config = quackamollie_settings.default_model_config
            model_manager = quackamollie_settings.default_model_manager
            model_manager_name = model_manager
            if model_manager:
                model_manager_class = model_managers_by_entrypoint_name.get(model_manager, None)
            else:
                model_manager_class = None

        # Get possible chat type override from database, if not already in a private chat
        if chat_type != ChatType.private:
            chat_type_override: Optional[ChatType] = chat_setting.chat_type_override
            if chat_type_override is not None:
                chat_type = chat_type_override

    if model_manager_class is None or model_manager_name is None:
        await message.answer("❌ No valid model manager is set for this chat. Please use /settings to set a model.")
        return

    if model_name is None:
        await message.answer("❌ No valid model name is set for this chat. Please use /settings to set a model.")
        return

    # Call the model manager to answer the message
    if chat_type == ChatType.private:
        await model_manager_class.request_model(model_manager_name, model_name, model_config, message)
    elif is_mentioned_in_group_or_supergroup(message, mention, chat_type):
        await model_manager_class.request_model(model_manager_name, model_name, model_config, message)
