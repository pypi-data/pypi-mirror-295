# -*- coding: utf-8 -*-
""" Module to define commands, handle additional configuration and start the bot """
__all__ = ["get_commands_list", "start_quackamollie_bot"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from click import BadParameter
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession
from typing import List

from quackamollie.core.bot.bot_info import QuackamollieBotData
from quackamollie.core.bot.callback.info_callback import info_router
from quackamollie.core.bot.callback.user_settings_callback import user_settings_router
from quackamollie.core.bot.callback.chat_settings_callback import chat_settings_router
from quackamollie.core.bot.callback.app_settings_callback import app_settings_router
from quackamollie.core.bot.command.history import history_router
from quackamollie.core.bot.command.reset import reset_router
from quackamollie.core.bot.command.settings_bot_command import settings_router
from quackamollie.core.bot.command.start_bot_command import start_router
from quackamollie.core.bot.command.message_by_id import message_by_id_router
from quackamollie.core.bot.handler.messages import message_router
from quackamollie.core.bot.middleware.user_filter import get_user_filter_outer_middleware_router
from quackamollie.core.cli.settings import QuackamollieSettings
from quackamollie.core.database.query.startup_query import (ensure_app_roles_registered_in_db,
                                                            ensure_bot_user_registered_in_db,
                                                            ensure_model_manager_types_registered_in_db)
from quackamollie.core.model_manager_registry.model_manager_registry import QuackamollieModelManagerRegistry

log = logging.getLogger(__name__)


def get_commands_list() -> List[BotCommand]:
    return [
        BotCommand(command="start", description="Start a new chat with Quackamollie"),
        BotCommand(command="settings", description="Access and change Quackamollie settings"),
        BotCommand(command="reset", description="Reset Chat"),
        BotCommand(command="history", description="Look through messages visible to the model"),
        BotCommand(command="message_by_id", description="Get the content of a message of the current chat from its ID"),
        # TODO: Improving settings will lead to using finite state machines, implement `/cancel` command to delete state
        # types.BotCommand(command="cancel", description="Cancel an active action"),
    ]


async def start_quackamollie_bot(settings: QuackamollieSettings, bot: Bot, dispatcher: Dispatcher,
                                 commands: List[BotCommand], engine: AsyncEngine,
                                 async_session: async_sessionmaker[AsyncSession]):
    """ Start the Quackamollie Telegram bot and close the database engine after polling ends

        :param settings: Quackamollie settings to pass between commands of quackamollie
        :type settings: QuackamollieSettings

        :param bot: The Telegram bot already initialized with token
        :type bot: Bot

        :param dispatcher: The aiogram dispatcher for messages and Telegram commands
        :type dispatcher: Dispatcher

        :param commands: The list of the Bot commands
        :type commands: List[BotCommand]

        :param engine: Database engine to dispose when the bot is stopped
        :type engine: AsyncEngine

        :param async_session: Database asynchronous session maker
        :type async_session: async_sessionmaker[AsyncSession]
    """
    # Ensure given default model name matches a model in the default model manager
    default_model_manager = settings.default_model_manager
    default_model = settings.default_model
    if default_model_manager is not None and default_model is not None:
        model_managers = QuackamollieModelManagerRegistry().model_managers
        model_list = await model_managers[default_model_manager].get_model_list()
        if default_model not in model_list:
            raise BadParameter(f"No model found with name '{default_model}' among models of the"
                               f" '{default_model_manager}' model manager. Available models"
                               f" are {', '.join(model_list)}.", param_hint="'--default-model'")

    # Add routers to the dispatcher
    dispatcher.include_router(get_user_filter_outer_middleware_router())
    dispatcher.include_router(start_router)
    dispatcher.include_router(settings_router)
    dispatcher.include_router(reset_router)
    dispatcher.include_router(history_router)
    dispatcher.include_router(message_by_id_router)
    dispatcher.include_router(info_router)
    dispatcher.include_router(user_settings_router)
    dispatcher.include_router(chat_settings_router)
    dispatcher.include_router(app_settings_router)
    dispatcher.include_router(message_router)
    log.debug("Routers added")

    await bot.set_my_commands(commands)
    log.debug("Commands set")

    quackamollie_bot_data = QuackamollieBotData()
    await quackamollie_bot_data.load_bot_info(bot)
    log.debug("QuackamollieBotData set")

    await ensure_app_roles_registered_in_db(async_session)
    log.debug("Database initialized with application roles")

    await ensure_bot_user_registered_in_db(async_session)
    log.debug("Database initialized with bot user")

    await ensure_model_manager_types_registered_in_db(async_session)
    log.debug("Database initialized with model managers types")

    log.debug("Start polling")
    await dispatcher.start_polling(bot, skip_update=True)

    # Close and clean-up pooled connections for database engine
    log.debug("Closing database engine")
    await engine.dispose()
