# -*- coding: utf-8 -*-
__all__ = ["get_user_filter_outer_middleware_router", "UserFilterMiddleware"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import json
import logging
import os

from aiogram import BaseMiddleware, Router
from aiogram.types import Message
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Set, Union

from quackamollie.core.bot.utils.bot_utils import ContextLock
from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.defaults import (DEFAULT_DATETIME_FORMAT, DEFAULT_USER_FILTER_MIDDLEWARE_INTERVAL_LIMIT,
                                        DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LIMIT,
                                        DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LOW_LIMIT)
from quackamollie.core.utils.str_management import sanitize_username

log = logging.getLogger(__name__)


class UserFilterMiddleware(BaseMiddleware):
    """ Manage and log unknown user activities, keep also a list of banned/blocked users. This middleware should
        be sufficient to ensure basic security against non-authorized.

        N.B: This project is thought to be executed locally and exposed on Telegram only to a limited set of users
        defined through configuration parsed by CLI.
     """

    USER_FILTER_LOCK: ContextLock = ContextLock()  # A lock to access and modify the class data asynchronously

    def __init__(self, data_dir: str, authorized_ids: Set[int], delete_banned_msg: bool, middleware_dir_name: str,
                 unauthorized_activity_file_name: str, banned_users_file_name: str,
                 datetime_format: str = DEFAULT_DATETIME_FORMAT,
                 interval_limit: int = DEFAULT_USER_FILTER_MIDDLEWARE_INTERVAL_LIMIT,
                 counter_low_limit: int = DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LOW_LIMIT,
                 counter_limit: int = DEFAULT_USER_FILTER_MIDDLEWARE_COUNTER_LIMIT):
        """ Initialize the middleware

            :param data_dir: Data directory dedicated to the current Quackamollie instance
            :type data_dir: str

            :param authorized_ids: A list of authorized Telegram IDs
            :type authorized_ids: Set[int]

            :param delete_banned_msg: Enable to delete messages sent from banned users, disable to just ignore them
            :type delete_banned_msg: bool

            :param middleware_dir_name: The directory where the middleware should save its files inside the `data_dir`
            :type middleware_dir_name: str

            :param unauthorized_activity_file_name: File name where unauthorized activities will be logged, unless the
                                                    user reaches limits and gets banned
            :type unauthorized_activity_file_name: str

            :param banned_users_file_name: File name where a list of banned users will be saved
            :type banned_users_file_name: str

            :param datetime_format: The format to user when exporting datetime objects to string
            :type datetime_format: str

            :param interval_limit: Time in seconds defining the interval between 2 messages under which a user will be
                                   declared as banned. Precisely, the rule is:
                                   if the user has sent the last 2 messages at an interval less than this value and
                                   at least `counter_low_limit` of messages have been sent, then the user is banned
            :type interval_limit: int

            :param counter_low_limit: The number of messages over which a user is declared as banned by the system,
                                      if these messages where sent consecutively in a short interval.
                                      Precisely, the rule is:
                                      if at least this number of messages have been sent and the user sent the last
                                      2 messages at an interval less than `interval_limit`, then the user is banned
            :type counter_low_limit: int

            :param counter_limit: The maximum number of messages over which a user is declared as banned
                                  by the system anyway
            :type counter_limit: int
        """
        self.data_dir: str = data_dir
        self.authorized_ids: Set[int] = authorized_ids
        self.authorized_str_ids: Set[str] = set(str(x) for x in self.authorized_ids)
        self.delete_banned_msg: bool = delete_banned_msg

        self.datetime_format: str = datetime_format
        self.interval_limit: int = interval_limit
        self.counter_low_limit: int = counter_low_limit
        self.counter_limit: int = counter_limit

        self.user_middleware_dir = os.path.join(data_dir, middleware_dir_name)
        os.makedirs(self.user_middleware_dir, exist_ok=True)

        self.fp_unauthorized_activity = os.path.join(self.user_middleware_dir, unauthorized_activity_file_name)
        self.fp_banned_users = os.path.join(self.user_middleware_dir, banned_users_file_name)
        self.unauthorized_activity: Dict[str, Dict[str, Union[int, str]]] = {}
        self.banned_users: Set[int] = set()

        if os.path.isfile(self.fp_unauthorized_activity):
            log.debug("Loading unauthorized activity from file")
            with open(self.fp_unauthorized_activity, 'r', encoding='utf-8') as fd_unauthorized_activity:
                self.unauthorized_activity = json.load(fd_unauthorized_activity)

        if os.path.isfile(self.fp_banned_users):
            log.debug("Loading banned users from file")
            with open(self.fp_banned_users, 'r', encoding='utf-8') as fd_banned_users:
                self.banned_users = set(json.load(fd_banned_users))

        # Ensure authorized users are not in the unauthorized_activity dict
        newly_authorized_users = self.authorized_str_ids & self.unauthorized_activity.keys()
        for new_user_id in newly_authorized_users:
            new_user_name = self.unauthorized_activity[new_user_id]['username']

            # The user was in unauthorized_activity, but they are now allowed. So we remove them from there
            # N.B: Banned users are still banned, if you want to un-ban them, change the ban file manually
            del self.unauthorized_activity[new_user_id]

            # Dump the modified json(s), so we can keep states between restarts
            with open(self.fp_unauthorized_activity, 'w') as fd_unauthorized_activity:
                json.dump(self.unauthorized_activity, fd_unauthorized_activity, indent=1)

            # Log the operation is done
            log.info(f"Newly authorized user '{new_user_name}' with ID '{new_user_id}' has been removed"
                     f" from the unauthorized activities list")

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        """ Execute middleware

            :param handler: Wrapped handler in middlewares chain
            :type handler: Callable[[Message, Dict[str, Any]]

            :param event: Incoming event (Subclass of :class:`aiogram.types.base.TelegramObject`)
            :type event: Message

            :param data: Contextual data. Will be mapped to handler arguments
            :type data: Dict[str, Any]

            :return: Nothing if the message is filtered or an await to the handler
            :rtype: Any
        """
        # Set variables before using context lock
        user_id: int = event.from_user.id
        user_str_id: str = str(user_id)  # Json dictionary keys must be str, so we cast the ID for this use
        new_user_in_unauthorized_activity: bool = False
        new_banned_user: bool = False
        new_msg_time = event.date.strftime(self.datetime_format)
        if event.from_user.username is not None:
            username = event.from_user.username
        else:
            username = event.from_user.full_name
        username = sanitize_username(username)

        # Using the ContextLock because accessing and modifying shared memory resources in async
        async with self.USER_FILTER_LOCK:
            if user_id in self.banned_users:  # using integer event ID for self.banned_users
                if self.delete_banned_msg:
                    return await event.delete()
                else:
                    return
            elif user_id not in self.authorized_ids:  # also int
                # Using the ContextLock because accessing and modifying shared memory resources in async
                if user_str_id in self.unauthorized_activity.keys():  # using str
                    log.warning(f"Unauthorized user '{username}' with ID '{user_id}' tries to communicate with system")
                    counter: int = self.unauthorized_activity[user_str_id]["counter"]
                    previous_time = datetime.strptime(self.unauthorized_activity[user_str_id]["last_msg_time"],
                                                      self.datetime_format)
                    interval = event.date.timestamp() - previous_time.timestamp()

                    if counter >= self.counter_limit or (
                            counter >= self.counter_low_limit and interval <= self.interval_limit
                    ):
                        new_banned_user = True
                        self.banned_users.add(user_id)  # The set uses int values
                        del self.unauthorized_activity[user_str_id]
                    else:
                        counter += 1
                        self.unauthorized_activity[user_str_id]["counter"] = counter
                        self.unauthorized_activity[user_str_id]["last_msg_time"] = new_msg_time

                else:
                    log.warning(f"Unauthorized unknown user '{username}' with ID '{user_id}' tries"
                                f" to communicate with the system")
                    new_user_in_unauthorized_activity = True
                    # We add the new user in unauthorized_activity
                    self.unauthorized_activity[user_str_id] = dict(username=username, counter=1,
                                                                   last_msg_time=new_msg_time)

                # Dump the modified json(s), so we can keep states between restarts
                with open(self.fp_unauthorized_activity, 'w') as fd_unauthorized_activity:
                    json.dump(self.unauthorized_activity, fd_unauthorized_activity, indent=1)

                if new_banned_user:
                    with open(self.fp_banned_users, 'w') as fd_banned_users:
                        json.dump(list(self.banned_users), fd_banned_users, indent=1)

        if user_id in self.authorized_ids:
            return await handler(event, data)
        elif new_user_in_unauthorized_activity:
            log.info(f"New user '{username}' with ID '{user_id}' has been added to the unauthorized"
                     f" activities list")
            return await event.answer("⚠ Access denied.\n\nThis is a private bot for private use. Try contacting the"
                                      " administrator if you know them, else please do NOT write to me again.")
        elif new_banned_user:
            # Additionally we could try calling functions as aiogram.methods.restrict_chat_member.RestrictChatMember
            # or aiogram.methods.ban_chat_member.BanChatMember, however I doubt it will work as expected since
            # these functions need the bot to have admin access. So for now, I don't do it.
            log.warning(f"User '{username}' with ID  '{user_id}' has been banned")
            return await event.answer("⛔ Access denied for too many requests. You are now officially banned"
                                      " from this bot and all your next messages will be totally ignored.")


def get_user_filter_outer_middleware_router(delete_banned_msg: bool = False, middleware_dir_name: str = "user_filter",
                                            unauthorized_activity_file_name: str = "unauthorized_activity.json",
                                            banned_users_file_name: str = "banned_users.json", **kwargs) -> Router:
    """ Get an aiogram router to a UserFilterMiddleware initialized from the click context and with given parameters.
        N.B: this middleware is registered as an outer middleware (cf. aiogram doc for more details)

        :param delete_banned_msg: This option deletes the messages sent by banned users
        :type delete_banned_msg: str

        :param middleware_dir_name: The directory where the middleware should save its files inside the ctx.data_dir
        :type middleware_dir_name: str

        :param unauthorized_activity_file_name: File name where unauthorized activities will be logged, unless the user
                                                reaches limits and gets banned
        :type unauthorized_activity_file_name: str

        :param banned_users_file_name: File name where banned users will be saved
        :type banned_users_file_name: str

        :param kwargs: Additional parameters to give to the UserFilterMiddleware constructor. For example:
                       * datetime_format="%Y.%m.%d-%H.%M.%S %z"
                       * interval_limit=2
                       * counter_limit=7
                       * counter_low_limit3  # Those are all default values
        :type kwargs: dict

        :return: A router connected to a UserFilterMiddleware initialized from click context
        :rtype: aiogram.Router
    """
    quackamollie_settings: QuackamollieSettings = get_settings_from_context()
    data_dir: str = quackamollie_settings.data_dir
    authorized_ids: Set[int] = quackamollie_settings.authorized_ids

    router = Router()
    user_filter_middleware = UserFilterMiddleware(data_dir, authorized_ids, delete_banned_msg, middleware_dir_name,
                                                  unauthorized_activity_file_name, banned_users_file_name, **kwargs)
    router.message.outer_middleware(user_filter_middleware)
    return router
