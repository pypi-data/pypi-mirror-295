# -*- coding: utf-8 -*-
__all__ = ["message_by_id_router", "command_message_by_id_handler"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import Message
from ast import literal_eval
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from quackamollie.core.bot.decorator.permissions import permission_authorized
from quackamollie.core.cli.settings import pass_quackamollie_settings, QuackamollieSettings
from quackamollie.core.bot.decorator.acknowledge_with_reactions import acknowledge_with_reactions
from quackamollie.core.database.model import ChatMessage

message_by_id_router = Router()


@message_by_id_router.message(Command("message_by_id"))
@permission_authorized
@acknowledge_with_reactions
@pass_quackamollie_settings
async def command_message_by_id_handler(quackamollie_settings: QuackamollieSettings, message: Message):
    """ Handler for the `/message_by_id` command in Telegram chat, show a message content from its ID

        :param quackamollie_settings: The application settings initialized from click context
        :type quackamollie_settings: QuackamollieSettings

        :param message: The message as given by aiogram router
        :type message: Message
    """
    # Get database session from settings
    async_session = quackamollie_settings.session

    # Get chat info from message
    chat_id: int = message.chat.id

    try:
        print(message.text)
        msg_id: int = literal_eval(str(message.text).replace("/message_by_id ", ""))
    except Exception:
        await message.answer("Bad formatting of identifier. Please use the command with"
                             " <code>/message_by_id MESSAGE_ID</code> where <code>MESSAGE_ID</code> is the ID of the"
                             " message you want to retrieve content from as given in brackets, i.e. '[]', by"
                             " the command /history",
                             parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return

    async with async_session() as session:
        chat_setting_result = await session.execute(select(ChatMessage).where(
            ChatMessage.id == msg_id
        ).where(
            ChatMessage.chat_id == chat_id
        ).options(
            selectinload(ChatMessage.user)
        ))
        chat_msg: Optional[ChatMessage] = chat_setting_result.scalars().first()

        if chat_msg:
            answer = f"[<code>{chat_msg.id}</code>] <code>{chat_msg.user.full_name}</code>: {chat_msg.content}"
            await message.answer(text=answer, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await message.answer(text=f"No message found in current chat with the ID '{msg_id}'")
