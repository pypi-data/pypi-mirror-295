# -*- coding: utf-8 -*-
__all__ = ["ModelFamilyIcon"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from enum import Enum


class ModelFamilyIcon(Enum):
    """ Quackamollie models family icons and short description based on name """
    LLAMA = "🦙"
    LLAMA_INDEX = "🦙☝️"
    LANGCHAIN = "🦜🔗"
    MULTIMODAL = "📷"
    AGENT = "🤖"
    CHAT = "💬"
    DEFAULT = "⭐️"

    @property
    def description(self):
        return self.name.lower().capitalize()
