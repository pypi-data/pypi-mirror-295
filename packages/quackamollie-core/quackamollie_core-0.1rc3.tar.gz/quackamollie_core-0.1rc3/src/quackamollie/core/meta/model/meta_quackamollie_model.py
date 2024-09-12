# -*- coding: utf-8 -*-
__all__ = ["MetaQuackamollieModel"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from abc import ABCMeta, abstractmethod
from typing import AsyncIterable, List, Optional, Tuple


class MetaQuackamollieModel(metaclass=ABCMeta):
    """ Metaclass for models managed by model managers """

    @classmethod
    @abstractmethod
    async def astream_answer(cls, content: str, chat_history: List, model_config: Optional[str] = None,
                             **kwargs) -> AsyncIterable[Tuple[str, bool]]:
        """ Asynchronous iterator to stream the answer from a LLM model

            :param content: The new message content
            :type content: str

            :param chat_history: A list of past messages formatted accordingly by model manager
            :type chat_history: List

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Optional[str]

            :param kwargs: Additional streaming arguments
            :type kwargs: Dict

            :return: An asynchronous iterator giving a tuple containing the new chunk and a boolean indicating
                     if the model is done or not
            :rtype: AsyncIterable[Tuple[str, bool]]
        """
        yield NotImplementedError("Abstract method 'astream_answer' not implemented.")
