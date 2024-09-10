# -*- coding: utf-8 -*-
__all__ = ["ChatType"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from enum import Enum


class ChatType(Enum):
    """ Types of Telegram chat and an additional type for local chats using command line devtools """
    private = "private"  # Telegram private chat
    group = "group"  # Telegram group
    supergroup = "supergroup"  # Telegram supergroup
    local = "local"  # Local chat using the command line "quackamollie chat [MODEL_MANAGER] [MODEL]", for tests

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
