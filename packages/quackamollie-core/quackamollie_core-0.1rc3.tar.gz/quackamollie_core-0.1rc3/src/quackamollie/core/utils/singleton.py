# -*- coding: utf-8 -*-
__all__ = ["Singleton"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "theheadofabroom", "Ashark", "agf", "danronmoon"]


class Singleton(type):
    """ Singleton metaclass (cf. https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python) """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ Returns always the same singleton instance """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
