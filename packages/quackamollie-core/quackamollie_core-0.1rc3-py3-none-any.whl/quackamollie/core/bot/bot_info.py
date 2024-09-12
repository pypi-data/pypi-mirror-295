# -*- coding: utf-8 -*-
__all__ = ["QuackamollieBotData"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from aiogram import Bot
from aiogram.types import User
from typing import Optional

from quackamollie.core.bot.utils.bot_utils import ContextLock
from quackamollie.core.utils.singleton import Singleton
from quackamollie.core.utils.str_management import sanitize_username


class QuackamollieBotDataBaseClass:
    """ This is an information object that is exposed as a singleton to keep dynamically loaded common bot info """

    BOT_DATA_LOCK: ContextLock = ContextLock()  # A lock to access and modify the class data asynchronously

    def __init__(self):
        self._bot_info: Optional[User] = None
        self._bot_id: Optional[int] = None
        self._bot_full_name: Optional[str] = None
        self._bot_username: Optional[str] = None
        self._bot_first_name: Optional[str] = None
        self._bot_last_name: Optional[str] = None
        self._bot_mention: Optional[str] = None

    async def load_bot_info(self, bot: Bot):
        """ Async loading of the bot info and save fields into current instance """
        bot_info = await bot.get_me()
        self._bot_info = bot_info
        self._bot_id = bot_info.id
        self._bot_full_name = sanitize_username(bot_info.full_name)
        self._bot_username = bot_info.username
        self._bot_first_name = sanitize_username(bot_info.first_name)
        self._bot_last_name = sanitize_username(bot_info.last_name)
        self._bot_mention = f"@{self._bot_username}"

    @property
    def bot_info(self) -> Optional[User]:
        return self._bot_info

    @property
    def bot_id(self) -> Optional[int]:
        return self._bot_id

    @property
    def bot_full_name(self) -> Optional[str]:
        return self._bot_full_name

    @property
    def bot_username(self) -> Optional[str]:
        return self._bot_username

    @property
    def bot_first_name(self) -> Optional[str]:
        return self._bot_first_name

    @property
    def bot_last_name(self) -> Optional[str]:
        return self._bot_last_name

    @property
    def bot_mention(self) -> Optional[str]:
        return self._bot_mention


class QuackamollieBotData(QuackamollieBotDataBaseClass, metaclass=Singleton):
    """ Singleton that stores bot additional info to dynamically retrieve and loaded at startup """
    pass
