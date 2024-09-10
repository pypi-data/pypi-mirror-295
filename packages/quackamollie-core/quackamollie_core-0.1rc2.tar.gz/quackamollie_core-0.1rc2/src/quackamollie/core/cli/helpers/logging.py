# -*- coding: utf-8 -*-
__all__ = ["callback_verbosity_count_to_logging_level"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click
import logging


def callback_verbosity_count_to_logging_level(_, param, value) -> int:
    """ Convert verbosity count from the option '--verbose' to_logging_level.

        :param _: The current click context

        :param param: The currently parsed parameter

        :param value: The number of 'v' appearing in the command line call (example: `'-vvvv' => 4`)
                      N.B: click option `count=True` ensures that this value is a positive integer
        :type value: int

        :return: A logging level value as defined in `logging.__init__` (example: `logging.DEBUG` level is 10)
        :rtype: int
    """
    if not isinstance(value, int):
        raise click.BadParameter(f"Value format should be a positive integer between 0 and 4 but it is {value}",
                                 param_hint=" / ".join([f"'{p}'" for p in param.opts]))

    match value:  # click option `count=True` ensures that this value is an integer >=0, so default case is DEBUG
        case 0:
            return logging.NOTSET
        case 1:
            return logging.ERROR
        case 2:
            return logging.WARN
        case 3:
            return logging.INFO
        case 4:
            return logging.DEBUG
        case _:
            return logging.DEBUG
