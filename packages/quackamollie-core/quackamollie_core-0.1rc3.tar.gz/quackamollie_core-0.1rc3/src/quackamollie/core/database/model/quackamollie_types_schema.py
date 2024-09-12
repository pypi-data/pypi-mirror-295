# -*- coding: utf-8 -*-
""" Module containing all tables of the `quackamollie_types` postgresql database schema """
__all__ = ["ModelManagerType"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI", "NanaBanana"]

from sqlalchemy import Column, Integer, String

from quackamollie.core.database.meta import Base


class ModelManagerType(Base):
    """ Table listing model managers loaded through entrypoints. It is autopopulated by the CLI at startup. """
    __tablename__ = "model_manager_types"
    __table_args__ = {'schema': 'quackamollie_types'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_manager_class = Column(String(320), nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}: id={self.id}, model_manager_class='{self.model_manager_class}'>"
