# -*- coding: utf-8 -*-
__all__ = ["ensure_user_chat_registered"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram.types import Message, CallbackQuery
from functools import wraps
from sqlalchemy import select
from typing import Callable, Union

from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.database.model import User, Chat


def ensure_user_chat_registered(func: Callable) -> Callable:
    """ Decorator to encapsulate aiogram message or query handlers in order to ensure that the user already registered
        using the `/start` command before calling the encapsulated handler. If not, it asks the user to register using
        the `/start` command.

        :param func: The function to encapsulate
        :type func: Callable

        :return: The encapsulated function
        :rtype: Callable
    """

    @wraps(func)
    async def user_chat_registered_wrapper(query_msg: Union[Message, CallbackQuery], *args, **kwargs):
        """ Encapsulate aiogram message or query handlers to ensure only requests from registered users are handled

            :param query_msg: Undifferentiated Message or CallbackQuery as given by aiogram router
            :type query_msg: Union[Message, CallbackQuery]
        """
        # Differentiate between queries and messages in order to get chat ID
        message: Message = query_msg.message if isinstance(query_msg, CallbackQuery) else query_msg

        user_id: int = query_msg.from_user.id
        chat_id: int = message.chat.id

        # Get settings for SQLAlchemy interaction
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()
        async_session = quackamollie_settings.session

        async with async_session() as session:
            user_result = await session.execute(select(User.id).where(User.id == user_id).limit(1))
            user = user_result.scalars().first()
            chat_result = await session.execute(select(Chat.id).where(Chat.id == chat_id).limit(1))
            chat = chat_result.scalars().first()

        # If IDs of user and chat can be retrieved from database, the request is forwarded to the encapsulated function
        if user is not None and chat is not None:
            return await func(query_msg, *args, **kwargs)
        else:  # Return a message stating to use the command '/start' when starting a new chat
            return await message.answer("⚠ The user or chat are not initialized, please run the command /start"
                                        " to initialize a new chat with me.")

    return user_chat_registered_wrapper
