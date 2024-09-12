# -*- coding: utf-8 -*-
""" Package to access all database models through a single entrypoint """
__all__ = ["User", "Chat", "ChatMember", "ChatSetting", "ChatMessage", "AppRole", "AppPermission",
           "ModelConfigPermission", "ModelConfig", "ModelManagerType"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "NanaBanana"]

from quackamollie.core.database.model.quackamollie_schema import (
    User, Chat, ChatMember, ChatSetting, ChatMessage, AppRole, AppPermission, ModelConfigPermission, ModelConfig
)
from quackamollie.core.database.model.quackamollie_types_schema import ModelManagerType
