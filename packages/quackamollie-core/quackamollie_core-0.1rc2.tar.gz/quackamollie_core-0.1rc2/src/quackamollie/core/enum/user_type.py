# -*- coding: utf-8 -*-
__all__ = ["UserType"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from enum import Enum


class UserType(Enum):
    """ Type of user embedded with message in the database to differentiate users and system messages """
    system = "SYSTEM"
    user = "USER"
