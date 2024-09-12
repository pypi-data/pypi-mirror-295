# -*- coding: utf-8 -*-
__all__ = ["history_router", "command_history_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.database.model import ChatMessage
from quackamollie.core.enum.user_type import UserType

history_router = Router()


@history_router.message(Command("history"))
@permission_authorized
@acknowledge_with_reactions
@pass_quackamollie_settings
async def command_history_handler(quackamollie_settings: QuackamollieSettings, message: Message):
    """ Handler for the `/history` command in Telegram chat, show context (messages history)

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
        if quackamollie_settings.history_max_length is None:
            chat_setting_result = await session.execute(select(ChatMessage).where(
                ChatMessage.chat_id == chat_id
            ).where(
                ChatMessage.active
            ).order_by(ChatMessage.sent_at_datetime.desc()).options(
                selectinload(ChatMessage.user)
            ))
        else:
            chat_setting_result = await session.execute(select(ChatMessage).where(
                ChatMessage.chat_id == chat_id
            ).where(
                ChatMessage.active
            ).limit(quackamollie_settings.history_max_length).order_by(ChatMessage.sent_at_datetime.desc()).options(
                selectinload(ChatMessage.user)
            ))
        chat_messages: Optional[List[ChatMessage]] = list(chat_setting_result.scalars().all())
        chat_messages.reverse()

        if chat_messages:
            if quackamollie_settings.history_max_length is None:
                answer: str = "<b>History</b> not limited\n"
            else:
                answer: str = f"<b>History</b> limited to {quackamollie_settings.history_max_length} messages\n"
            for msg in chat_messages:
                answer += f"\n[<code>{msg.id}</code>] <code>{msg.user.full_name}</code>: "
                if len(msg.content) <= 75:
                    answer += msg.content.replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;").replace("&",
                                                                                                               "&amp;")
                else:
                    answer += msg.content[:75].replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;"
                                                                                               ).replace("&", "&amp;")
                    answer += " [...]"
                if msg.user.user_type == UserType.system:
                    answer += "\n"
            await message.answer(text=answer, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await message.answer(text="No history in current chat")
