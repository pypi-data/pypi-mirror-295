# -*- coding: utf-8 -*-
__all__ = ["AppRoleType"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from enum import Enum


class AppRoleType(Enum):
    """ Application roles attributed to users by IDs using the command line options.
        `disallowed` allows removing rights for the user while keeping information in the database.
        To remove users data, the user should call `/delete_account` in its private chat with the bot or admin can call
        the dedicated database function or command line.
    """
    system = "SYSTEM"
    admin = "ADMIN"
    moderator = "MODERATOR"
    authorized = "AUTHORIZED"
    unauthorized = "UNAUTHORIZED"
