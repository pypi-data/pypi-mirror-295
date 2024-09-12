# -*- coding: utf-8 -*-
__all__ = ["get_commands_from_entry_points"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click

from importlib.metadata import entry_points
from typing import Dict, Union


def get_commands_from_entry_points(entrypoint_group: str) -> Dict[str, Union[click.Command, click.Group,
                                                                             click.MultiCommand]]:
    """ Parse entry_points from a group in order to load and make dynamically available click commands, groups or
        multi-commands to a parent group or multi-command

        :param entrypoint_group: The entry_point group to iterate over to dynamically find quackamollie click plugins
        :type entrypoint_group: str

        :return: A dictionary of click commands, groups or multi-commands indexed by entry_point name
        :rtype: Dict[str, Union[click.Command, click.Group, click.MultiCommand]]
    """
    commands = {}

    # Iterate over entrypoint group
    for script in entry_points(group=entrypoint_group):
        # Loading the entrypoint, failing raises an AttributeError
        try:
            command_or_group = script.load()
        except Exception as error:
            raise AttributeError(f"Error loading command or group from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" with exception:\n{error}")

        # Ensure loaded entrypoint matches expected click types, failing raises an AttributeError
        if (isinstance(command_or_group, click.Command) or isinstance(command_or_group, click.Group)
                or isinstance(command_or_group, click.MultiCommand)):
            commands[script.name] = command_or_group
        else:
            raise AttributeError(f"Error loaded class '{command_or_group.__name__}', from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" doesn't inherit from click Command or Group or MultiCommand.")

    return commands
