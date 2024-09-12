# -*- coding: utf-8 -*-
__all__ = ["generate_timestamp_version"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from datetime import datetime


def generate_timestamp_version() -> str:
    """ Generate a timestamp from current time

        :return: A string formatted as a timestamp, with format `%y.%m.%d-%H.%M.%S`
        :rtype: str
    """
    return datetime.now().strftime("%y.%m.%d-%H.%M.%S")
