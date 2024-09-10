# -*- coding: utf-8 -*-
__all__ = ["camel_to_snake", "sanitize_username"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "nimish"]

import re

from typing import Optional

regex_special_characters: re.Pattern = re.compile(r"[\"'{}()\[\]`]")


def camel_to_snake(s: str) -> str:
    """ Convert CamelCase string to snake_case. Function from https://stackoverflow.com/a/44969381

        :param s: A CamelCase string
        :type s: str

        :return: A snake_case string
        :rtype: str
    """
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')


def sanitize_username(input_str: Optional[str]) -> Optional[str]:
    """ Sanitize a string from username or assimilated data in order to export it safely to Json format.
        It doesn't really mater if there is data loss because the user is referenced by user ID,
        it is more to give an idea of whom this is than its exact name

        :param input_str: The string to sanitize
        :type input_str: Optional[str]

        :return: The sanitized string
        :rtype: Optional[str]
    """
    return None if input_str is None else regex_special_characters.sub("", input_str)
