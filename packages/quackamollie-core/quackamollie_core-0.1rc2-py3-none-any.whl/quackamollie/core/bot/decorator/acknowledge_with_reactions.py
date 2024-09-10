# -*- coding: utf-8 -*-
__all__ = ["acknowledge_with_reactions"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram.types import Message, ReactionTypeEmoji
from functools import wraps, partial
from typing import Any, Callable, Optional, Union

from quackamollie.core.defaults import DEFAULT_READ_REACTION_EMOJI, DEFAULT_ANSWERED_REACTION_EMOJI

log = logging.getLogger(__name__)


def acknowledge_with_reactions(func: Optional[Callable] = None, enable_read_reaction: bool = True,
                               read_reaction_emoji: str = DEFAULT_READ_REACTION_EMOJI,
                               enable_answered_reaction: bool = True,
                               answered_reaction_emoji: str = DEFAULT_ANSWERED_REACTION_EMOJI) -> Callable:
    """ Decorator to encapsulate aiogram message handlers in order to automatically react with emojis
        to the message sent when entering the decorator and after calling the encapsulated function.
        If the given argument is not an `aiogram.types.Message`, no reactions are emitted.

        :param func: The function to encapsulate, if None the decorator returns a partial instead
        :type func: Optional[Callable]

        :param enable_read_reaction: Enable reaction when receiving the message
        :type enable_read_reaction: bool

        :param read_reaction_emoji: The emoji to use when receiving the message
        :type read_reaction_emoji: str

        :param enable_answered_reaction: Enable reaction after the call of the decorated function
        :type enable_answered_reaction: bool

        :param answered_reaction_emoji: The emoji to use after calling the decorated function
        :type answered_reaction_emoji: str

        :return: The decorated function or a partial if `func` argument is `None`
        :rtype: Callable
    """

    if func is None:
        return partial(acknowledge_with_reactions, enable_read_reaction=enable_read_reaction,
                       read_reaction_emoji=read_reaction_emoji, enable_answered_reaction=enable_answered_reaction,
                       answered_reaction_emoji=answered_reaction_emoji)

    @wraps(func)
    async def acknowledge_with_reactions_wrapper(msg: Union[Message, Any], *args, **kwargs):
        """ Encapsulate aiogram message to acknowledge receiving it and when we finish treating it

            :param msg: A Message or any other type given by aiogram
            :type msg: Union[Message, Any]
        """
        # Only react to messages, not other Types
        if isinstance(msg, Message):
            if enable_read_reaction:
                # Let know the user through reaction that we are parsing its message
                await msg.react([ReactionTypeEmoji(emoji=read_reaction_emoji)])

            # Call decorated function
            await func(msg, *args, **kwargs)

            if enable_answered_reaction:
                # Change reaction to say we finished treatments
                await msg.react([ReactionTypeEmoji(emoji=answered_reaction_emoji)])
        else:
            # Call decorated function
            await func(msg, *args, **kwargs)

    return acknowledge_with_reactions_wrapper
