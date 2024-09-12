# -*- coding: utf-8 -*-
""" This module contains tools to set configuration in CLI and access it as read only during async execution """

__all__ = ["get_settings_from_context", "QuackamollieSettings", "pass_quackamollie_settings"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import click
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from pydantic import BaseModel, computed_field, ConfigDict, Field
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession
from typing import Any, Dict, List, Optional, Set

from quackamollie.core.defaults import (DEFAULT_CONFIG_FILE, DEFAULT_LOG_DIR, DEFAULT_VERBOSITY, DEFAULT_DATA_DIR,
                                        DEFAULT_OLLAMA_BASE_URL, DEFAULT_DB_PROTOCOL, DEFAULT_DB_HOST, DEFAULT_DB_NAME,
                                        DEFAULT_HISTORY_MAX_LENGTH, DEFAULT_MIN_NB_CHUNK_TO_SHOW)

log = logging.getLogger(__name__)

SET_DISABLED_ERROR_FORMAT = ("Unable to set variable '{}' at runtime, `enable_config_edition` is False.\n"
                             "If you want to store dynamic data at runtime you are invited to do so by storing"
                             " them into the database or, alternatively, store them using QuackamollieBotData"
                             " and its associated ContextLock (with `async with`). Dynamically setting"
                             " QuackamollieBotData is to use scarcely and with caution.")


class QuackamollieSettings(BaseModel):
    """ This is an information object that is used to set inferred config in CLI and then read it in
        aiogram async functions. To avoid the use of ContextLock at runtime and because configuration should not
        dynamically change, setting values is disabled after synchron initialization by the CLI.
        Note that:

        - this object must have an empty constructor in order to be embedded as a click pass decorator, so all fields
          should have defaults

        - if you want to store dynamic data at runtime you are invited to do so by storing them into the SQL database
          or other custom solutions you may implement
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Allow types like Bot, AsyncEngine, etc.

    enable_settings_edition: bool = Field(default=True)
    raise_error_when_not_editable: bool = Field(default=True)
    _config_file: Optional[str] = DEFAULT_CONFIG_FILE
    _config: Optional[Dict[str, Any]] = None
    _logging_config: Optional[Dict[str, Any]] = None
    _log_dir: Optional[str] = DEFAULT_LOG_DIR
    _verbose: int = DEFAULT_VERBOSITY
    _bot_token: Optional[str] = None
    _admin_ids: List[int] = []
    _moderator_ids: List[int] = []
    _user_ids: List[int] = []
    _authorized_ids: Set[int] = set()
    _data_dir: Optional[str] = DEFAULT_DATA_DIR
    _ollama_base_url: Optional[str] = DEFAULT_OLLAMA_BASE_URL
    _default_model_manager: Optional[str] = None
    _default_model: Optional[str] = None
    _default_model_config: Optional[str] = None
    _history_max_length: Optional[int] = DEFAULT_HISTORY_MAX_LENGTH
    _min_nb_chunk_to_show: int = DEFAULT_MIN_NB_CHUNK_TO_SHOW
    _db_protocol: str = DEFAULT_DB_PROTOCOL
    _db_username: Optional[str] = None
    _db_password: Optional[str] = None
    _db_host: str = DEFAULT_DB_HOST
    _db_port: Optional[int] = None
    _db_name: str = DEFAULT_DB_NAME
    _db_url: Optional[str] = None
    _anonymized_db_url: Optional[str] = None
    _bot: Optional[Bot] = None
    _dispatcher: Optional[Dispatcher] = None
    _commands: List[BotCommand] = []
    _engine: Optional[AsyncEngine] = None
    _session: Optional[async_sessionmaker[AsyncSession]] = None
    _additional_config: Optional[Dict[str, Any]] = None

    def _ensure_property_is_editable(self, property_name: str) -> bool:
        if self.enable_settings_edition:
            return True
        elif self.raise_error_when_not_editable:
            raise RuntimeError(SET_DISABLED_ERROR_FORMAT.format(property_name))
        else:
            log.error(SET_DISABLED_ERROR_FORMAT.format(property_name))
            return False

    @computed_field
    @property
    def config_file(self) -> Optional[str]:  # converted to a `property` by `computed_field`
        """ Path of the application's configuration file

            :return: The application's configuration file path
            :rtype: Optional[str]
        """
        return self._config_file

    @config_file.setter
    def config_file(self, new_config_file: Optional[str]) -> None:
        if self._ensure_property_is_editable('config_file'):
            self._config_file = new_config_file

    @computed_field
    @property
    def config(self) -> Optional[Dict[str, Any]]:
        """ The configuration imported from the configuration file in the form of a dictionary

            :return: The configuration parsed from configuration file path
            :rtype: Optional[Dict[str, Any]]
        """
        return self._config

    @config.setter
    def config(self, new_config: Optional[Dict[str, Any]]) -> None:
        if self._ensure_property_is_editable('config'):
            self._config = new_config

    @computed_field
    @property
    def logging_config(self) -> Optional[Dict[str, Any]]:
        """ The 'logging' configuration imported from the configuration file in the form of a dictionary

            :return: The 'logging' configuration parsed from configuration file path
            :rtype: Optional[Dict[str, Any]]
        """
        return self._logging_config

    @logging_config.setter
    def logging_config(self, new_logging_config: Optional[Dict[str, Any]]) -> None:
        if self._ensure_property_is_editable('logging_config'):
            self._logging_config = new_logging_config

    @computed_field
    @property
    def log_dir(self) -> Optional[str]:
        """ Directory path for logs

            :return: Directory path for logs
            :rtype: Optional[str]
        """
        return self._log_dir

    @log_dir.setter
    def log_dir(self, new_log_dir: Optional[str]) -> None:
        if self._ensure_property_is_editable('log_dir'):
            self._log_dir = new_log_dir

    @computed_field
    @property
    def verbose(self) -> int:
        """ Effective verbosity level in the same format as logging

            :return: The verbosity level
            :rtype: int
        """
        return self._verbose

    @verbose.setter
    def verbose(self, new_verbosity: int) -> None:
        if self._ensure_property_is_editable('verbose'):
            self._verbose = new_verbosity

    @computed_field
    @property
    def bot_token(self) -> Optional[str]:
        """ Telegram bot API token

            :return: The API token for the Telegram bot
            :rtype: Optional[str]
        """
        return self._bot_token

    @bot_token.setter
    def bot_token(self, new_bot_token: Optional[str]) -> None:
        if self._ensure_property_is_editable('bot_token'):
            self._bot_token = new_bot_token

    @computed_field
    @property
    def anonymized_bot_token(self) -> Optional[str]:
        """ Telegram bot API token with sensitive information replaced by '*'. We show the last 3 digits of the user
            part of the token so the admin can check if the token used matches what is expected

            :return: The API token for the Telegram bot with sensitive information replaced by '*'
            :rtype: Optional[str]
        """
        if self._bot_token is None:
            return None
        else:
            u, p = self._bot_token.split(':')
            return '*' * len(u[:-3]) + u[-3:] + ':' + '*' * len(p)

    @computed_field
    @property
    def admin_ids(self) -> List[int]:
        """ A list of admin Telegram IDs

            :return: A list, empty by default, of admin IDs as integers
            :rtype: List[int]
        """
        return self._admin_ids

    @admin_ids.setter
    def admin_ids(self, new_admin_ids: List[int]) -> None:
        if self._ensure_property_is_editable('admin_ids'):
            self._admin_ids = new_admin_ids
            self._authorized_ids.update(self._admin_ids)

    @computed_field
    @property
    def anonymized_admin_ids(self) -> List[str]:
        """ The list of admin IDs with sensitive information replaced by '*'. We show the last 3 digits of the IDs,
            so we can check if the list matches what is expected

            :return: The list of admin IDs with sensitive information replaced by '*'
            :rtype: List[str]
        """
        return ['*' * len(str(admin_id)[:-3]) + str(admin_id)[-3:] for admin_id in self._admin_ids]

    @computed_field
    @property
    def moderator_ids(self) -> List[int]:
        """ A list of moderator Telegram IDs

            :return: A list, empty by default, of moderator IDs as integers
            :rtype: List[int]
        """
        return self._moderator_ids

    @moderator_ids.setter
    def moderator_ids(self, new_moderator_ids: List[int]) -> None:
        if self._ensure_property_is_editable('moderator_ids'):
            self._moderator_ids = new_moderator_ids
            self._authorized_ids.update(self._moderator_ids)

    @computed_field
    @property
    def anonymized_moderator_ids(self) -> List[str]:
        """ The list of moderator IDs with sensitive information replaced by '*'. We show the last 3 digits of the IDs,
            so we can check if the list matches what is expected

            :return: The list of moderator IDs with sensitive information replaced by '*'
            :rtype: List[str]
        """
        return ['*' * len(str(moderator_id)[:-3]) + str(moderator_id)[-3:] for moderator_id in self._moderator_ids]

    @computed_field
    @property
    def user_ids(self) -> List[int]:
        """ A list of user Telegram IDs

            :return: A list, empty by default, of user IDs as integers
            :rtype: List[int]
        """
        return self._user_ids

    @user_ids.setter
    def user_ids(self, new_user_ids: List[int]) -> None:
        if self._ensure_property_is_editable('user_ids'):
            self._user_ids = new_user_ids
            self._authorized_ids.update(self._user_ids)

    @computed_field
    @property
    def anonymized_user_ids(self) -> List[str]:
        """ The list of user IDs with sensitive information replaced by '*'. We show the last 3 digits of the IDs,
            so we can check if the list matches what is expected

            :return: The list of user IDs with sensitive information replaced by '*'
            :rtype: List[str]
        """
        return ['*' * len(str(user_id)[:-3]) + str(user_id)[-3:] for user_id in self._user_ids]

    @computed_field
    @property
    def authorized_ids(self) -> Set[int]:
        """ The list of all authorized Telegram IDs inferred from admin, moderator and user Telegram IDs

            :return: A list, empty by default, of all authorized IDs as integers
            :rtype: Set[int]
        """
        return self._authorized_ids

    @computed_field
    @property
    def anonymized_authorized_ids(self) -> Set[str]:
        """ The list of all authorized IDs with sensitive information replaced by '*'. We show the last 3 digits
            of the IDs, so we can check if the list matches what is expected

            :return: The list of all authorized IDs with sensitive information replaced by '*'
            :rtype: Set[str]
        """
        return {'*' * len(str(authorized_id)[:-3]) + str(authorized_id)[-3:] for authorized_id in self._authorized_ids}

    @computed_field
    @property
    def data_dir(self) -> Optional[str]:
        """ Directory path dedicated to Quackamollie's data

            :return: Directory path dedicated to Quackamollie's data
            :rtype: Optional[str]
        """
        return self._data_dir

    @data_dir.setter
    def data_dir(self, new_data_dir: Optional[str]) -> None:
        if self._ensure_property_is_editable('data_dir'):
            self._data_dir = new_data_dir

    @computed_field
    @property
    def ollama_base_url(self) -> Optional[str]:
        """ Ollama base URL

            :return: The Ollama base URL
            :rtype: Optional[str]
        """
        return self._ollama_base_url

    @ollama_base_url.setter
    def ollama_base_url(self, new_ollama_base_url: Optional[str]) -> None:
        if self._ensure_property_is_editable('ollama_base_url'):
            self._ollama_base_url = new_ollama_base_url

    @computed_field
    @property
    def default_model_manager(self) -> Optional[str]:
        """ The name of the ModelManager to use by default

            :return: The name of the ModelManager to use by default
            :rtype: Optional[str]
        """
        return self._default_model_manager

    @default_model_manager.setter
    def default_model_manager(self, new_default_model_manager: Optional[str]) -> None:
        if self._ensure_property_is_editable('default_model_manager'):
            self._default_model_manager = new_default_model_manager

    @computed_field
    @property
    def default_model(self) -> Optional[str]:
        """ The name of the model to use by default

            :return: The name of the model to use by default
            :rtype: Optional[str]
        """
        return self._default_model

    @default_model.setter
    def default_model(self, new_default_model: Optional[str]) -> None:
        if self._ensure_property_is_editable('default_model'):
            self._default_model = new_default_model

    @computed_field
    @property
    def default_model_config(self) -> Optional[str]:
        """ The additional configuration for instantiation of the default model

            :return: Additional configuration of the model to use by default
            :rtype: Optional[str]
        """
        return self._default_model_config

    @default_model_config.setter
    def default_model_config(self, new_default_model_config: Optional[str]) -> None:
        if self._ensure_property_is_editable('default_model_config'):
            self._default_model_config = new_default_model_config

    @computed_field
    @property
    def history_max_length(self) -> Optional[int]:
        """ Maximum length of the history, in number of messages including those previously generated, to include
            when answering a message using a model. If None, no limit is applied during the request to the database.

            :return: The maximum length of the history to include when answering a message using a model
            :rtype: Optional[int]
        """
        return self._history_max_length

    @history_max_length.setter
    def history_max_length(self, new_history_max_length: Optional[int]) -> None:
        if self._ensure_property_is_editable('history_max_length'):
            self._history_max_length = new_history_max_length

    @computed_field
    @property
    def min_nb_chunk_to_show(self) -> int:
        """ Minimum number of chunks to show at the same time when streaming the answer of a model.
            A value of 10 implies trying the edition of the generated Telegram message every 10 chunks.

            :return: The minimum number of chunks to show at the same time when streaming the answer of a model
            :rtype: int
        """
        return self._min_nb_chunk_to_show

    @min_nb_chunk_to_show.setter
    def min_nb_chunk_to_show(self, new_min_nb_chunk_to_show: int) -> None:
        if self._ensure_property_is_editable('min_nb_chunk_to_show'):
            self._min_nb_chunk_to_show = new_min_nb_chunk_to_show

    @computed_field
    @property
    def db_protocol(self) -> str:
        """ Database protocol, must be a protocol supported by SQLAlchemy

            :return: The database protocol
            :rtype: str
        """
        return self._db_protocol

    @db_protocol.setter
    def db_protocol(self, new_db_protocol: str) -> None:
        if self._ensure_property_is_editable('db_protocol'):
            self._db_protocol = new_db_protocol

    @computed_field
    @property
    def db_username(self) -> Optional[str]:
        """ Username for postgres database connection

            :return: The username for postgres database connection
            :rtype: Optional[str]
        """
        return self._db_username

    @db_username.setter
    def db_username(self, new_db_username: Optional[str]) -> None:
        if self._ensure_property_is_editable('db_username'):
            self._db_username = new_db_username

    @computed_field
    @property
    def anonymized_db_username(self) -> Optional[str]:
        """ The username for postgres database connection with sensitive information replaced by '*'. We show the
            last 3 digits of the username, so we can check if the list matches what is expected

            :return: The username for postgres database connection with sensitive information replaced by '*'
            :rtype: Optional[str]
        """
        if self._db_username is None:
            return None
        else:
            return self._db_username[:2] + '****'

    @computed_field
    @property
    def db_password(self) -> Optional[str]:
        """ Password for postgres database connection

            :return: The password for postgres database connection
            :rtype: Optional[str]
        """
        return self._db_password

    @db_password.setter
    def db_password(self, new_db_password: Optional[str]) -> None:
        if self._ensure_property_is_editable('db_password'):
            self._db_password = new_db_password

    @computed_field
    @property
    def anonymized_db_password(self) -> Optional[str]:
        """ The password for postgres database connection with sensitive information replaced by '*'.

            :return: The password for postgres database connection with sensitive information replaced by '*'
            :rtype: Optional[str]
        """
        if self._db_password is None:
            return None  # We divulge if the password is set or not
        else:
            return '****'  # Constant string to not divulge anything else about password strength

    @computed_field
    @property
    def db_host(self) -> str:
        """ Hostname of the postgres database

            :return: The hostname of the postgres database
            :rtype: str
        """
        return self._db_host

    @db_host.setter
    def db_host(self, new_db_host: str) -> None:
        if self._ensure_property_is_editable('db_host'):
            self._db_host = new_db_host

    @computed_field
    @property
    def db_port(self) -> Optional[int]:
        """ Port of the postgres database

            :return: The port of the postgres database
            :rtype: Optional[int]
        """
        return self._db_port

    @db_port.setter
    def db_port(self, new_db_port: Optional[int]) -> None:
        if self._ensure_property_is_editable('db_port'):
            self._db_port = new_db_port

    @computed_field
    @property
    def db_name(self) -> str:
        """ Name of the postgres database

            :return: The name of the postgres database
            :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, new_db_name: str) -> None:
        if self._ensure_property_is_editable('db_name'):
            self._db_name = new_db_name

    @computed_field
    @property
    def db_url(self) -> Optional[str]:
        """ URL of the postgres database

            :return: The URL of the postgres database
            :rtype: Optional[str]
        """
        return self._db_url

    @db_url.setter
    def db_url(self, new_db_url: Optional[str]) -> None:
        if self._ensure_property_is_editable('db_url'):
            self._db_url = new_db_url

    @computed_field
    @property
    def anonymized_db_url(self) -> Optional[str]:
        """ URL of the postgres database

            :return: The URL of the postgres database
            :rtype: Optional[str]
        """
        return self._anonymized_db_url

    @anonymized_db_url.setter
    def anonymized_db_url(self, new_anonymized_db_url: Optional[str]) -> None:
        if self._ensure_property_is_editable('anonymized_db_url'):
            self._anonymized_db_url = new_anonymized_db_url

    @computed_field
    @property
    def bot(self) -> Optional[Bot]:
        """ Telegram bot, typically initialized from given Telegram API token

            :return: The Telegram bot
            :rtype: Optional[Bot]
        """
        return self._bot

    @bot.setter
    def bot(self, new_bot: Optional[Bot]) -> None:
        if self._ensure_property_is_editable('bot'):
            self._bot = new_bot

    @computed_field
    @property
    def dispatcher(self) -> Optional[Dispatcher]:
        """ Telegram dispatcher

            :return: The Telegram dispatcher
            :rtype: Optional[Dispatcher]
        """
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, new_dispatcher: Optional[Dispatcher]) -> None:
        if self._ensure_property_is_editable('dispatcher'):
            self._dispatcher = new_dispatcher

    @computed_field
    @property
    def commands(self) -> List[BotCommand]:
        """ Telegram bot commands list

            :return: The list of commands for the Telegram bot
            :rtype: List[BotCommand]
        """
        return self._commands

    @commands.setter
    def commands(self, new_commands: List[BotCommand]) -> None:
        if self._ensure_property_is_editable('commands'):
            self._commands = new_commands

    @computed_field
    @property
    def engine(self) -> Optional[AsyncEngine]:
        """ SQLAlchemy Engine for database requests, initialized by CLI with database config

            :return: The SQLAlchemy Engine
            :rtype: Optional[AsyncEngine]
        """
        return self._engine

    @engine.setter
    def engine(self, new_engine: Optional[AsyncEngine]) -> None:
        if self._ensure_property_is_editable('engine'):
            self._engine = new_engine

    @computed_field
    @property
    def session(self) -> Optional[async_sessionmaker[AsyncSession]]:
        """ SQLAlchemy async session maker for async database requests, initialized by CLI for use in aiogram functions

            :return: The SQLAlchemy async session maker
            :rtype: Optional[async_sessionmaker[AsyncSession]]
        """
        return self._session

    @session.setter
    def session(self, new_session: Optional[async_sessionmaker[AsyncSession]]) -> None:
        if self._ensure_property_is_editable('session'):
            self._session = new_session

    @computed_field
    @property
    def additional_config(self) -> Optional[Dict[str, Any]]:
        """ Used to store additional configuration, i.e. tokens/URL/data given through CLI and constant through runtime

            :return: The additional configuration fields given through CLI unknown options
            :rtype: Optional[Dict[str, Any]]
        """
        return self._additional_config

    @additional_config.setter
    def additional_config(self, new_additional_config: Optional[Dict[str, Any]]) -> None:
        if self._ensure_property_is_editable('additional_config'):
            self._additional_config = new_additional_config


# Function decorator that passes 'QuackamollieSettings' object
pass_quackamollie_settings = click.make_pass_decorator(QuackamollieSettings, ensure=True)


def get_settings_from_context(no_error: bool = False) -> Optional[QuackamollieSettings]:
    """ Get the current instance of QuackamollieSettings. If `no_error` is True, exceptions will be caught and logged,
        else it raises RuntimeErrors if no click context is found or if no object is defined in the click context.

        :return: The current instance of QuackamollieSettings
        :rtype: Optional[QuackamollieSettings]
    """
    if no_error:
        try:
            ctx = click.get_current_context()
        except RuntimeError as exc:
            log.warning(f"No click context was found at runtime and the following error was caught:\n{exc}")
            return None
    else:
        ctx = click.get_current_context()

    quackamollie_settings: Optional[QuackamollieSettings] = ctx.obj
    if quackamollie_settings is None:
        if no_error:
            log.warning("No valid QuackamollieSettings was found in click context at runtime")
            return None
        else:
            raise RuntimeError("No valid QuackamollieSettings was found in click context at runtime")
    else:
        return quackamollie_settings
