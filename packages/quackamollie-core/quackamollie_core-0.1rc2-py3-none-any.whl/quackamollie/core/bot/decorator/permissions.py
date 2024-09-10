# -*- coding: utf-8 -*-
__all__ = ["permission_authorized", "permission_moderator", "permission_admin"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram.types import Message, CallbackQuery
from functools import wraps
from typing import Callable, Optional, Union

from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.enum.chat_type import ChatType

log = logging.getLogger(__name__)


def permission_authorized(func: Callable) -> Callable:
    """ Decorator to encapsulate aiogram message or query handlers in order to ensure only requests
        from authorized users are handled

        :param func: The function to encapsulate
        :type func: Callable

        :return: The encapsulated function
        :rtype: Callable
    """

    @wraps(func)
    async def authorized_wrapper(arg: Union[Message, CallbackQuery], *args, **kwargs):
        """ Encapsulate aiogram message or query handlers to ensure only requests from authorized users are handled

            :param arg: A Message or CallbackQuery given by aiogram
            :type arg: Union[Message, CallbackQuery]
        """
        # Get settings to check IDs
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()

        # If the user is authorized, the request is forwarded to the encapsulated function
        if arg.from_user.id in quackamollie_settings.authorized_ids:
            return await func(arg, *args, **kwargs)
        else:  # Log an error and return a message stating access denied
            # Differentiate between queries and messages in order to improve resulting error
            if isinstance(arg, CallbackQuery):
                query: Optional[CallbackQuery] = arg
                message: Message = arg.message
            else:
                query: Optional[CallbackQuery] = None
                message: Message = arg

            # Log error group or supergroup chats
            if message.chat.type == ChatType.supergroup.value or message.chat.type == ChatType.group.value:
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{arg.from_user.id}' tried to"
                          f" reference me in the {message.chat.type} chat '{message.chat.title}' and was rejected.")
            else:  # Log error for private chats
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{arg.from_user.id}' tried to"
                          f" chat with me in its private chat and was rejected.")

            # Keeping the answer short for queries because they are shown as popups
            if query is not None:
                return await query.answer("Access Denied")
            else:
                return await message.answer("⚠ Access Denied\nYou're not authorized to interact with me.")

    return authorized_wrapper


def permission_moderator(func: Callable) -> Callable:
    """ Decorator to encapsulate aiogram message or query handlers in order to ensure only requests
        from moderator users are handled

        :param func: The function to encapsulate
        :type func: Callable

        :return: The encapsulated function
        :rtype: Callable
    """

    @wraps(func)
    async def moderator_wrapper(arg: Union[Message, CallbackQuery], *args, **kwargs):
        """ Encapsulate aiogram message or query handlers to ensure only requests from moderator users are handled

            :param arg: A Message or CallbackQuery given by aiogram
            :type arg: Union[Message, CallbackQuery]
        """
        # Get settings to check IDs
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()
        user_id: int = arg.from_user.id

        # If the user is a moderator, the request is forwarded to the encapsulated function
        if user_id in quackamollie_settings.moderator_ids or user_id in quackamollie_settings.admin_ids:
            return await func(arg, *args, **kwargs)
        else:  # Log an error and return a message stating access denied
            # Differentiate between queries and messages in order to improve resulting error
            if isinstance(arg, CallbackQuery):
                query: Optional[CallbackQuery] = arg
                message: Message = arg.message
            else:
                query: Optional[CallbackQuery] = None
                message: Message = arg

            # Log error group or supergroup chats
            if message.chat.type == ChatType.supergroup.value or message.chat.type == ChatType.group.value:
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{user_id}' tried to"
                          f" perform a moderator action in the {message.chat.type} chat '{message.chat.title}' and"
                          f" was rejected.")
            else:  # Log error for private chats
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{user_id}' tried to"
                          f" perform a moderator action in private chat and was rejected.")

            # Keeping the answer short for queries because they are shown as popups
            if query is not None:
                return await query.answer("Moderator Access Denied")
            else:
                return await message.answer("⚠ Moderator Access Denied\n"
                                            "You're not authorized to perform moderator actions.")

    return moderator_wrapper


def permission_admin(func: Callable) -> Callable:
    """ Decorator to encapsulate aiogram message or query handlers in order to ensure only requests
        from admin users are handled

        :param func: The function to encapsulate
        :type func: Callable

        :return: The encapsulated function
        :rtype: Callable
    """

    @wraps(func)
    async def admin_wrapper(arg: Union[Message, CallbackQuery], *args, **kwargs):
        """ Encapsulate aiogram message or query handlers to ensure only requests from admin users are handled

            :param arg: A Message or CallbackQuery given by aiogram
            :type arg: Union[Message, CallbackQuery]
        """
        # Get settings to check IDs
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()

        # If the user is an admin, the request is forwarded to the encapsulated function
        if arg.from_user.id in quackamollie_settings.admin_ids:
            return await func(arg, *args, **kwargs)
        else:  # Log an error and return a message stating access denied
            # Differentiate between queries and messages in order to improve resulting error
            if isinstance(arg, CallbackQuery):
                query: Optional[CallbackQuery] = arg
                message: Message = arg.message
            else:
                query: Optional[CallbackQuery] = None
                message: Message = arg

            # Log error group or supergroup chats
            if message.chat.type == ChatType.supergroup.value or message.chat.type == ChatType.group.value:
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{arg.from_user.id}' tried to"
                          f" perform an admin action in the {message.chat.type} chat '{message.chat.title}' and"
                          f" was rejected.")
            else:  # Log error for private chats
                log.error(f"Unauthorized user '{arg.from_user.full_name}' with ID '{arg.from_user.id}' tried to"
                          f" perform an admin action in private chat and was rejected.")

            # Keeping the answer short for queries because they are shown as popups
            if query is not None:
                return await query.answer("Admin Access Denied")
            else:
                return await message.answer("⛔ Admin Access Denied\n"
                                            "You're not authorized to perform admin actions.")

    return admin_wrapper
