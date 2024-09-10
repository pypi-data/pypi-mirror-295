# -*- coding: utf-8 -*-
__all__ = ["reset_router", "command_reset_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy import select
from typing import List, Optional

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.database.model import ChatMessage

reset_router = Router()


@reset_router.message(Command("reset"))
@permission_authorized
@acknowledge_with_reactions
@pass_quackamollie_settings
async def command_reset_handler(quackamollie_settings: QuackamollieSettings, message: Message):
    """ Handler for the `/reset` command in Telegram chat, wipes context (messages history)

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param message: The message as given by aiogram router
        :type message: Message
    """
    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get chat info from message
    chat_id: int = message.chat.id

    async with async_session() as session:
        chat_setting_result = await session.execute(select(ChatMessage).where(
            ChatMessage.chat_id == chat_id
        ).where(
            ChatMessage.active
        ))
        chat_messages: Optional[List[ChatMessage]] = list(chat_setting_result.scalars().all())

        if chat_messages:
            for msg in chat_messages:
                msg.active = False
            await session.commit()
            await message.answer(text="Chat has been reset")
        else:
            await message.answer(text="No history in current chat")
