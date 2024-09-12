# -*- coding: utf-8 -*-
""" Module for SQLAlchemy bases """
__all__ = ["Base", "TimeStampedModel"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from datetime import datetime
from sqlalchemy import MetaData, Column, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    """ Declarative base for SQLAlchemy Postgresql database with async access using `AsyncAttrs` """
    metadata = MetaData(schema='quackamollie', naming_convention=NAMING_CONVENTION)


class TimeStampedModel(Base):
    """ Extension of the base model with creation and update dates columns """
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
