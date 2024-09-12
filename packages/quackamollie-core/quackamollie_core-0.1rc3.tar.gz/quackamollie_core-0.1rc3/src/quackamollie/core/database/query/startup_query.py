# -*- coding: utf-8 -*-
__all__ = ["ensure_app_roles_registered_in_db", "ensure_bot_user_registered_in_db",
           "ensure_model_manager_types_registered_in_db"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Dict, Type

from quackamollie.core.bot.bot_info import QuackamollieBotData
from quackamollie.core.database.model import AppRole, ModelManagerType, User
from quackamollie.core.enum.role_type import AppRoleType
from quackamollie.core.enum.user_type import UserType
from quackamollie.core.meta.model_manager.meta_quackamollie_model_manager import MetaQuackamollieModelManager
from quackamollie.core.model_manager_registry.model_manager_registry import (
    QuackamollieModelManagerRegistry
)

log = logging.getLogger(__name__)


async def ensure_app_roles_registered_in_db(async_session: async_sessionmaker[AsyncSession]):
    """ Ensure that the application roles are registered in the Database, i.e. an AppRole row exists for every value
        of AppRoleType

        :param async_session: The async session maker associated to the initialized database engine
        :type async_session: async_sessionmaker[AsyncSession]
    """
    async with async_session() as session:
        async with session.begin():
            app_role_to_create = []

            # Create a role for each element of AppRoleType enum, if role doesn't exist already
            for role_type in AppRoleType:
                log.debug(f"role_type={role_type}")
                role_result = await session.execute(select(AppRole.id).where(AppRole.role_type == role_type).limit(1))
                log.debug(f"role_result={role_result}")
                role_id = role_result.scalars().first()
                log.debug(f"role_id={role_id}")

                if role_id is None:
                    log.debug(f"The AppRole '{role_type.value}' is not found in the database. Creating it...")
                    app_role_to_create.append(AppRole(role_type=role_type))
                else:
                    log.debug(f"AppRole '{role_type.value}' already exists in the database with ID '{role_id}'")

            if app_role_to_create:
                session.add_all(app_role_to_create)


async def ensure_bot_user_registered_in_db(async_session: async_sessionmaker[AsyncSession]):
    """ Ensure that the current bot is registered in the Database as a SYSTEM user

        :param async_session: The async session maker associated to the initialized database engine
        :type async_session: async_sessionmaker[AsyncSession]
    """
    quackamollie_bot_data = QuackamollieBotData()
    async with async_session() as session:
        bot_user_result = await session.execute(select(User.id).where(User.id == quackamollie_bot_data.bot_id).limit(1))
        bot_user_id = bot_user_result.scalars().first()
        role_result = await session.execute(select(AppRole.id).where(AppRole.role_type == AppRoleType.system).limit(1))
        system_role_id = role_result.scalars().one()

    # Create a user for the bot if not found
    if bot_user_id is None:
        log.debug("The bot user is not found in the database. Creating them...")
        new_bot_user = User(id=quackamollie_bot_data.bot_id, user_type=UserType.system, app_role_id=system_role_id,
                            full_name=quackamollie_bot_data.bot_full_name,
                            username=quackamollie_bot_data.bot_username,
                            first_name=quackamollie_bot_data.bot_first_name,
                            last_name=quackamollie_bot_data.bot_last_name)
        async with async_session() as session:
            async with session.begin():
                session.add(new_bot_user)
    else:
        log.debug(f"Bot user '{quackamollie_bot_data.bot_username}' with ID '{quackamollie_bot_data.bot_id}'"
                  f" already exists in the database")


async def ensure_model_manager_types_registered_in_db(async_session: async_sessionmaker[AsyncSession]):
    """ Ensure that the loaded model manager types are registered in the Database in the dedicated table in types schema

        :param async_session: The async session maker associated to the initialized database engine
        :type async_session: async_sessionmaker[AsyncSession]
    """
    model_managers: Dict[str, Type[MetaQuackamollieModelManager]] = QuackamollieModelManagerRegistry().model_managers

    async with async_session() as session:
        async with session.begin():
            model_manager_type_to_create = []

            # Convert all keys of this dict to rows in quackamollie_types
            for model_manager_class in model_managers.values():
                model_manager_class_name = model_manager_class.__name__
                model_manager_type_result = await session.execute(select(ModelManagerType.id).where(
                    ModelManagerType.model_manager_class == model_manager_class_name
                ).limit(1))
                model_manager_type_id = model_manager_type_result.scalars().first()

                if model_manager_type_id is None:
                    log.debug(f"The ModelManagerType '{model_manager_class_name}' is not found in the database."
                              f" Creating it...")
                    model_manager_type_to_create.append(ModelManagerType(model_manager_class=model_manager_class_name))
                else:
                    log.debug(f"ModelManagerType '{model_manager_class_name}' already exists in the database"
                              f" with ID '{model_manager_type_id}'")

            if model_manager_type_to_create:
                session.add_all(model_manager_type_to_create)
